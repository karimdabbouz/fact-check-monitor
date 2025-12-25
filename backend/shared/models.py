from sqlalchemy import Column, String, Integer, DateTime, UniqueConstraint
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.ext.declarative import declarative_base
import datetime


Base = declarative_base()


class FactCheckArticles(Base):
    __tablename__ = 'fact_check_articles'
    __table_args__ = (UniqueConstraint('url', name='constraint_fact_check_articles'),)

    id = Column(Integer, primary_key=True, autoincrement=True)
    url = Column(String, nullable=False)
    medium = Column(String)
    category = Column(String)
    author = Column(String)
    kicker = Column(String)
    headline = Column(String)
    teaser = Column(String)
    body = Column(JSONB)
    image_url = Column(String)
    published_at = Column(DateTime)
    topic = Column(String)
    claim = Column(String)
    instrumentalizer = Column(String)
    entities = Column(JSONB)
    last_updated = Column(DateTime, default=datetime.datetime.now(datetime.UTC))