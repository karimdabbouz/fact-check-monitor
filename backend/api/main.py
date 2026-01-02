from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from shared.services.fact_check_articles_service import FactCheckArticlesService
from shared.schemas import TopicCount, FactCheckArticlesSchema
from shared.database import Database
from typing import List, Optional
import datetime

app = FastAPI()
db = Database()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get('/')
def read_root():
    return {'message': 'Faktencheck-Aggregator API', 'version': '1.0'}


@app.get('/topic-counts', response_model=List[TopicCount])
def get_topic_counts(
        published_after: Optional[str] = None,
        published_before: Optional[str] = None,
        medium: Optional[str] = None
    ) -> List[TopicCount]:
    '''
    Retrieve a list of topic counts for a given time period and optional medium.
    Query parameters:
    - published_after: Date in YYYY-MM-DD format (optional)
    - published_before: Date in YYYY-MM-DD format (optional)
    - medium: Fact-checking medium filter (optional)
    '''
    with db.get_session() as session:
        service = FactCheckArticlesService(session)
        published_after_dt = None
        published_before_dt = None
        if published_after:
            try:
                published_after_dt = datetime.datetime.strptime(published_after, '%Y-%m-%d')
            except ValueError:
                pass
        if published_before:
            try:
                published_before_dt = datetime.datetime.strptime(published_before, '%Y-%m-%d')
                published_before_dt = published_before_dt.replace(hour=23, minute=59, second=59)
            except ValueError:
                pass
        topic_counts = service.get_topic_counts_by_period(
            published_after=published_after_dt,
            published_before=published_before_dt,
            medium=medium
        )
        return topic_counts


@app.get('/articles-by-topic', response_model=List[FactCheckArticlesSchema])
def get_articles_by_topic(
        topic: str,
        published_after: Optional[str] = None,
        published_before: Optional[str] = None,
        medium: Optional[str] = None,
        limit: int = 100
    ) -> List[FactCheckArticlesSchema]:
    '''
    Retrieve articles for a given topic with optional filtering by time period and medium.
    Query parameters:
    - topic: Topic name (required)
    - published_after: Date in YYYY-MM-DD format (optional)
    - published_before: Date in YYYY-MM-DD format (optional)e
    - medium: Fact-checking medium filter (optional)
    - limit: Maximum number of articles to return (default: 100)
    '''
    with db.get_session() as session:
        service = FactCheckArticlesService(session)
        published_after_dt = None
        published_before_dt = None
        if published_after:
            try:
                published_after_dt = datetime.datetime.strptime(published_after, '%Y-%m-%d')
            except ValueError:
                pass
        if published_before:
            try:
                published_before_dt = datetime.datetime.strptime(published_before, '%Y-%m-%d')
                published_before_dt = published_before_dt.replace(hour=23, minute=59, second=59)
            except ValueError:
                pass
        articles = service.get_articles(
            limit=limit,
            medium=medium,
            topic=topic,
            published_after=published_after_dt,
            published_before=published_before_dt
        )
        return articles