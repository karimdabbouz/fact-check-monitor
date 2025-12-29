from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from shared.services.fact_check_articles_service import FactCheckArticlesService
from shared.schemas import TopicCount
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
        
        # Convert date strings to datetime objects
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
                # Set to end of day
                published_before_dt = published_before_dt.replace(hour=23, minute=59, second=59)
            except ValueError:
                pass
        
        topic_counts = service.get_topic_counts_by_period(
            published_after=published_after_dt,
            published_before=published_before_dt,
            medium=medium
        )
        return topic_counts