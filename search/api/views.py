from django_elasticsearch_dsl_drf.filter_backends import SearchFilterBackend
from django_elasticsearch_dsl_drf.viewsets import DocumentViewSet
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from elasticsearch import Elasticsearch
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.reverse import reverse
from rest_framework.views import APIView

from core.pagination import CustomPagination

from ..documents import NewsPostIndex, StockRecordIndex
from .serializers import NewsPostIndexSerializer, StockRecordIndexSerializer


class SearchAPIRootView(APIView):
    permission_classes = [AllowAny]

    @swagger_auto_schema(auto_schema=None, tags=["Search"])
    def get(self, request, format=None):
        return Response(
            {
                "stockrecord": reverse(
                    "stockrecorddocument-api-list", request=request, format=format
                ),
                "newsrecord": reverse(
                    "newsrecorddocument-api-list", request=request, format=format
                ),
            }
        )


class StockRecordViewset(DocumentViewSet):
    document = StockRecordIndex
    serializer_class = StockRecordIndexSerializer
    filter_backends = [SearchFilterBackend]
    pagination_class = CustomPagination
    lookup_field = "id"
    search_fields = {
        "title": {"fuzziness": "AUTO"},
        "summary": {"fuzziness": "AUTO"},
    }

    @swagger_auto_schema(
        tags=["Search"],
    )
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)


class NewsPostViewset(DocumentViewSet):
    document = NewsPostIndex
    serializer_class = NewsPostIndexSerializer
    filter_backends = [SearchFilterBackend]
    pagination_class = CustomPagination
    lookup_field = "id"
    search_fields = {
        "title": {"fuzziness": "AUTO"},
        "description": {"fuzziness": "AUTO"},
    }

    @swagger_auto_schema(
        tags=["Search"],
    )
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)


class NewsPostSuggestAPIView(APIView):
    permission_classes = [AllowAny]

    @swagger_auto_schema(
        tags=["Search"],
        operation_description="Autocomplete news post titles",
        manual_parameters=[
            openapi.Parameter(
                "search",
                openapi.IN_QUERY,
                type=openapi.TYPE_STRING,
                required=True,
            ),
        ],
        responses={200: openapi.Response(description="List of suggestion strings")},
    )
    def get(self, request, *args, **kwargs):
        query = request.query_params.get("search", "").strip()

        if not query:
            return Response

        es = Elasticsearch(hosts=["http://localhost:9200"])

        suggest_body = {
            "suggest": {
                "title_suggest": {
                    "prefix": query,
                    "completion": {
                        "field": "title_suggest",
                        "fuzzy": {"fuzziness": "AUTO"},
                    },
                }
            }
        }

        try:
            result = es.search(index="news_posts", body=suggest_body)
            options = result["suggest"]["title_suggest"][0]["options"]
            suggestions = [opt["text"] for opt in options if "_source" in opt]
            return Response(suggestions)

        except Exception as e:
            return Response({"error": str(e)}, status=500)
