from django.urls import include, path
from rest_framework.routers import SimpleRouter

from .views import (
    NewsPostSuggestAPIView,
    NewsPostViewset,
    SearchAPIRootView,
    StockRecordViewset,
)

router = SimpleRouter()
router.register(r"stockrecord", StockRecordViewset, basename="stockrecorddocument-api")
router.register(r"newsrecord", NewsPostViewset, basename="newsrecorddocument-api")

urlpatterns = [
    path("", SearchAPIRootView.as_view(), name="api-search"),
    path("documents/", include(router.urls)),
    path("suggest/news/", NewsPostSuggestAPIView.as_view(), name="news-suggest"),
]
