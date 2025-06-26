from celery import shared_task

from .services.announcement import AnnouncementScraper
from .services.stock_news import StockNews


@shared_task(name="stock scheduling")
def stocknews_scraping():
    scrape = StockNews()
    return scrape.stock_news()


@shared_task(name="announcement")
def announcement_scraping():
    announcement = AnnouncementScraper()
    return announcement.extract_announcement()
