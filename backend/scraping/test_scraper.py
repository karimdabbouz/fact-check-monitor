import sys, datetime
from pathlib import Path
from zoneinfo import ZoneInfo
from selenium.webdriver.common.by import By

project_root = str(Path(__file__).parent.parent)
sys.path.append(project_root)

from news_scraper.news_scraper.scraper import ArticleLinkScraper, ArticleContentScraper


def close_cookie_consent_correctiv(driver):
    shadow_host = driver.find_element(By.XPATH, '//div[@id="cmpwrapper"]')
    shadow_root = driver.execute_script("return arguments[0].shadowRoot", shadow_host)
    driver.execute_script("""
    return arguments[0].shadowRoot.querySelector('a.cmptxt_btn_yes');
    """, shadow_host).click()


def main():
    article_content_scraper = ArticleContentScraper(
        scraping_mode='FRONTEND',
        selenium_settings={
            'mode': 'uc',
            'headed': True,
            'proxy': None
        },
        link_list=['https://correctiv.org/faktencheck/2025/08/01/berliner-oepnv-was-tatsaechlich-rund-um-pfefferspray-gilt-auf1-waffenverbot/'],
        medium='correctiv',
        pre_hooks=[lambda driver: close_cookie_consent_correctiv(driver)],
        datetime_published_selector=('//time', False, lambda element: datetime.datetime.strptime(element.get_attribute('datetime').split('+')[0], '%Y-%m-%dT%H:%M:%S') - datetime.timedelta(hours=(lambda: 2 if datetime.datetime.now(ZoneInfo('Europe/Brussels')).dst() != datetime.timedelta(0) else 1)())),
        # post_hooks=[lambda driver, article_data: parse_factcheck_data(driver, article_data), lambda driver, article_data: parse_category(driver, article_data)],
        # author_selector=('//p[@class="detail__authors"]', False, lambda element: element.text.replace('von ', '')),
        image_url_selector=('//article//source', False, lambda element: element.get_attribute('srcset')),
        kicker_selector=('//header/span[@class="topline"]', False, lambda element: element.text),
        headline_selector=('//header/h1', False, lambda element: element.text),
        teaser_selector=('//header/p[@class="detail__excerpt"]', False, lambda element: element.text),
        body_selector=('//div[@class="detail__content"]/p', True, lambda element: [x.text for x in element if 'Alle Faktenchecks zu' not in x.text and 'Redigatur:' not in x.text]),
        subheadlines_selector=('//div[@class="detail__content"]/h2', True, lambda element: [x.text for x in element])
    )
    articles = article_content_scraper.run()
    print(f'Scraped {len(articles)} articles.')
    
    # RSS
    # article_link_scraper = ArticleLinkScraper(
    #     scraping_mode='RSS',
    #     selenium_settings={
    #         'mode': 'uc',
    #         'headed': True,
    #         'proxy': None
    #     },
    #     urls=['https://www.nius.de/rss'],
    #     article_url_selector=None
    # )
    # API
    # article_link_scraper = ArticleLinkScraper(
    #     scraping_mode='API',
    #     selenium_settings={
    #         'mode': 'wire',
    #         'headed': True,
    #         'proxy': None
    #     },
    #     urls=['https://correctiv.org/wp-json/wp/v2/posts?categories=5&per_page=5'],
    #     article_url_selector=lambda x: [entry['link'] for entry in x]
    # )
    # try:
    #     links = article_link_scraper.run()
    #     print(f"{len(links)} found")
    # except Exception as e:
    #     print(f"ArticleLinkScraper raised an exception: {e}")
    pass

if __name__ == "__main__":
    main()
