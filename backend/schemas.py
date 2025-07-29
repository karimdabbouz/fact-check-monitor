from pydantic import BaseModel
from typing import int, List, Optional
import datetime


class Paragraph(BaseModel):
    subheadline: Optional[str] = None
    text: str


class Body(BaseModel):
    paragraphs: List[Paragraph]


class FactCheckArticlesSchema(BaseModel):
    '''
    Equivalent to the db schema
    '''
    id: int = None
    url: str = None
    source: str = None
    kicker: str = None
    headline: str = None
    teaser: str = None
    body: Body = None
    published_at: datetime.datetime = None
    llm_generated_topic: str = None
    topic: str = None
    last_updated: datetime.datetime = None
