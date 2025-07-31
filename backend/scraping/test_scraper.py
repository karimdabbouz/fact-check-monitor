import sys
from pathlib import Path

project_root = str(Path(__file__).parent.parent)
sys.path.append(project_root)

from news_scraper.news_scraper.scraper import ArticleLinkScraper



def main():
    # Minimal test: instantiate and run ArticleLinkScraper for a public RSS feed
    article_link_scraper = ArticleLinkScraper(
        scraping_mode='RSS',
        selenium_settings={
            'mode': 'uc',
            'headed': True,
            'proxy': None
        },
        urls=['https://www.nius.de/rss'],
        article_url_selector=None
    )
    try:
        links = article_link_scraper.run()
        print(f"{len(links)} found")
    except Exception as e:
        print(f"ArticleLinkScraper raised an exception: {e}")

if __name__ == "__main__":
    main()
