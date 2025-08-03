from pydantic import BaseModel
from typing import List, Optional, Dict, Any, Literal, Union
import datetime


class ParagraphBlock(BaseModel):
    type: Literal['paragraph']
    text: str

class SubheadlineBlock(BaseModel):
    type: Literal['subheadline']
    text: str

BodyBlock = Union[ParagraphBlock, SubheadlineBlock]


class FactCheckArticlesSchema(BaseModel):
    '''
    Equivalent to the db schema
    '''
    id: int = None
    url: str = None
    medium: str = None
    category: Optional[str] = None
    author: Optional[str] = None
    kicker: Optional[str] = None
    headline: Optional[str] = None
    teaser: Optional[str] = None
    body: List[BodyBlock] = None
    image_url: Optional[str] = None
    published_at: Optional[datetime.datetime] = None
    llm_generated_topic: Optional[str] = None
    topic: Optional[str] = None
    last_updated: datetime.datetime = None

    @classmethod
    def from_news_scraper(cls, article: Dict[str, Any]) -> 'FactCheckArticlesSchema':
        article = article.copy()
        if 'body_structured' in article and isinstance(article['body_structured'], List):
            body = []
            for entry in article['body_structured']:
                if entry[0] == 'subheadline':
                    body_block = SubheadlineBlock(
                        type='subheadline',
                        text=entry[1]
                    )
                else:
                    body_block = ParagraphBlock(
                        type='paragraph',
                        text=entry[1]
                    )
                body.append(body_block)
            article['body'] = body
        if 'datetime_published' in article:
            article['published_at'] = article['datetime_published']
        return cls(**article)

    class Config:
        extra = 'ignore'
