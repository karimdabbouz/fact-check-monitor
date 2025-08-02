from sqlalchemy import Column, String, Integer, DateTime
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.ext.declarative import declarative_base
import datetime


Base = declarative_base()


class FactCheckArticles(Base):
    __tablename__ = 'fact_check_articles'

    id = Column(Integer, primary_key=True, autoincrement=True)
    url = Column(String, nullable=False)
    medium = Column(String)
    category = Column(String)
    author = Column(String)
    kicker = Column(String)
    headline = Column(String)
    teaser = Column(String)
    body = Column(JSONB)
    image_url = Column(str)
    published_at = Column(DateTime)
    llm_generated_topic = Column(String)
    topic = Column(String)
    last_updated = Column(DateTime, default=datetime.datetime.now(datetime.UTC))