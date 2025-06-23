import json

from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand
from django.utils.text import slugify

from news.models import Category, NewsPost

User = get_user_model()


class Command(BaseCommand):
    help = "Load sample news from a JSON file"

    def handle(self, *args, **kwargs):
        try:
            with open("sample_news.json", "r") as f:
                news_data = json.load(f)
        except FileNotFoundError:
            self.stderr.write("❌ sample_news.json not found.")
            return

        creator = User.objects.first()

        if not creator:
            self.stderr.write("❌ Make sure at least one User exists.")
            return

        for item in news_data:
            category_name = item.get("category")
            if category_name:
                category_obj, created = Category.objects.get_or_create(
                    name=category_name
                )
            else:
                category_obj = None

            post = NewsPost.objects.create(
                title=item["title"],
                description=item["description"],
                slug=slugify(item["title"]),
                category=category_obj,
                status="published",
                creator=creator,
            )
            post.tags.add(*item.get("tags", []))

        self.stdout.write(self.style.SUCCESS("✅ Sample news successfully loaded!"))
