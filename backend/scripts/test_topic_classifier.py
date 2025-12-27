import sys, asyncio
from pathlib import Path
from typing import Optional
import argparse

project_root = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(project_root))

from shared.database import Database
from shared.models import FactCheckArticles
from shared.schemas import FactCheckArticleContent, Topic
from shared.agents.topic_classifier import TopicClassifierAgent

async def classify_article_cli(article_id: int, model_name: Optional[str] = None):
    """
    CLI function to classify a single article by ID using the TopicClassifierAgent.
    """
    db = Database()
    
    with db.get_session() as session:
        article_orm = session.query(FactCheckArticles).filter_by(id=article_id).first()

        if not article_orm:
            print(f"Error: Article with ID {article_id} not found in the database.")
            return
        
        article_content = FactCheckArticleContent(
            kicker=article_orm.kicker if article_orm.kicker else "",
            headline=article_orm.headline if article_orm.headline else "",
            teaser=article_orm.teaser if article_orm.teaser else "",
            body=article_orm.body if article_orm.body else []
        )

        print(f"Classifying article ID: {article_id} - Headline: {article_orm.headline[:70]}...")
        
        classifier_agent = TopicClassifierAgent(model_name=model_name)
        
        try:
            classified_topic: Topic = await classifier_agent.run(article_content)
            print(f"✅ Classified Topic: {classified_topic.topic_label}")
        except Exception as e:
            print(f"❌ Error classifying article {article_id}: {e}")


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description="Classify a single fact-check article using the TopicClassifierAgent."
    )
    parser.add_argument(
        "article_id",
        type=int,
        help="The ID of the article to classify."
    )
    parser.add_argument(
        "--model",
        dest="model_name",
        type=str,
        default=None,
        help="Optional: Specify a different LLM model name (e.g., 'anthropic/claude-3-opus-20240229:beta')."
    )
    
    args = parser.parse_args()
    asyncio.run(classify_article_cli(article_id=args.article_id, model_name=args.model_name))