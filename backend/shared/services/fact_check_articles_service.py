import sys
from pathlib import Path

project_root = str(Path(__file__).parent.parent)
sys.path.append(project_root)

from shared.schemas import FactCheckArticlesSchema
from shared.models import FactCheckArticles
from typing import List, Dict, Any, Optional


class FactCheckArticlesService:
    '''
    Service for handling operations on the FactCheckArticles table.
    '''

    def __init__(self, db_session):
        '''Initialize with a database session.'''
        self.db_session = db_session


    def get_article(self, article_id: int) -> Optional[FactCheckArticles]:
        '''Retrieve a FactCheckArticle by ID.'''
        pass


    def update_article(self, article_id: int, update_data: Dict[str, Any]) -> Optional[FactCheckArticles]:
        '''Update an existing FactCheckArticle.'''
        pass


    def delete_article(self, article_id: int) -> bool:
        '''Delete a FactCheckArticle by ID.'''
        pass


    def list_articles(self, limit: int = 100, offset: int = 0) -> List[FactCheckArticles]:
        '''List FactCheckArticles with pagination.'''
        pass


    def save_articles(self, articles: List[FactCheckArticlesSchema]):
        '''
        Bulk insert a list of FactCheckArticlesSchema objects into the database,
        skipping articles whose URLs already exist.
        '''
        urls = [article.url for article in articles if article.url]
        existing_urls = set(
            url for (url,) in self.db_session.query(FactCheckArticles.url)
            .filter(FactCheckArticles.url.in_(urls))
            .all()
        )
        new_articles = [article for article in articles if article.url not in existing_urls]
        article_objs = [FactCheckArticles(**article.model_dump(exclude_unset=True)) for article in new_articles]
        self.db_session.bulk_save_objects(article_objs)
        self.db_session.commit()


    def get_missing_urls(self, urls: List[str]) -> List[str]:
        '''
        Given a list of URLs, return only those that are not already present in the database.
        '''
        if not urls:
            return []
        existing_urls = set(
            url for (url,) in self.db_session.query(FactCheckArticles.url)
            .filter(FactCheckArticles.url.in_(urls))
            .all()
        )
        return [url for url in urls if url not in existing_urls]