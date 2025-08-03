from backend.schemas import FactCheckArticlesSchema
from backend.models import FactCheckArticles
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


    def save_articles(self, articles: List[FactCheckArticlesSchema]) -> None:
        '''
        Bulk insert a list of FactCheckArticlesSchema objects into the database.
        '''
        article_objs = [FactCheckArticles(**article.model_dump(exclude_unset=True)) for article in articles]
        self.db_session.bulk_save_objects(article_objs)
        self.db_session.commit()