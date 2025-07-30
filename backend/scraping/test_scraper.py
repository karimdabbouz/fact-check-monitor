from news_scraper import ArticleLinkScraper

def main():
    # Minimal test: instantiate and run ArticleLinkScraper for a public RSS feed
    article_link_scraper = ArticleLinkScraper(
        scraping_mode='RSS',
        proxy=None,
        selenium_mode='wire',
        selenium_headed=False,
        urls=['https://www.nius.de/rss'],
        article_url_selector=None
    )
    try:
        links = article_link_scraper.run()
        print(f"Links found: {links}")
    except Exception as e:
        print(f"ArticleLinkScraper raised an exception: {e}")

if __name__ == "__main__":
    main()
