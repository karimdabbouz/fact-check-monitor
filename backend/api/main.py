from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from shared.services.fact_check_articles_service import FactCheckArticlesService
from shared.schemas import TopicCount
from shared.database import Database
from typing import List, Optional
import datetime

app = FastAPI()
db = Database()

@app.get('/')
def read_root():
    return {'message': 'Faktencheck-Aggregator API', 'version': '1.0'}


@app.get('/topic-counts', response_model=List[TopicCount])
def get_topic_counts(
        published_after: Optional[datetime.datetime] = None,
        published_before: Optional[datetime.datetime] = None,
        medium: Optional[str] = None
    ) -> List[TopicCount]:
    '''
    TODO
    Retrieve a list of topic counts for a given time period and optional medium.
    '''
    with db.get_session() as session:
        service = FactCheckArticlesService(session)
        topic_counts = service.get_topic_counts_by_period(
            published_after=published_after,
            published_before=published_before,
            medium=medium
        )
        return topic_counts




# @app.post('/users', response_model=UserResponse, status_code=status.HTTP_201_CREATED)
# def create_user(user_data: UserCreate):
#     '''
#     Creates a user entry in the user table using the e-mail address.
#     Will use OAuth in production.
#     '''
#     with db.get_session() as session:
#         existing = session.query(User).filter(User.email == user_data.email).first()
#         if existing:
#             raise HTTPException(status_code=400, detail='This email already exists')

#         user = User(email = user_data.email)
#         session.add(user)
#         session.commit()
#         session.refresh(user)
#         return UserResponse.model_validate(user)