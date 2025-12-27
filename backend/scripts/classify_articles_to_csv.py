import sys, asyncio
from pathlib import Path
from typing import Optional, List, Dict, Any
import argparse
import pandas as pd

# Add the Python project root to sys.path
python_project_root = Path(__file__).resolve().parent.parent # Points to /backend/
if str(python_project_root) not in sys.path:
    sys.path.insert(0, str(python_project_root))

from shared.database import Database
from shared.models import FactCheckArticles
from shared.schemas import FactCheckArticleContent, Topic
from shared.agents.topic_classifier import TopicClassifierAgent

async def classify_articles_to_csv_cli(num_articles: int, output_csv: str, model_name: Optional[str] = None):
    """
    CLI function to load N articles, classify them using the TopicClassifierAgent,
    and save the results to a CSV file.
    """
    db = Database()
    results = []
    
    print(f"Fetching {num_articles} articles from the database...")
    with db.get_session() as session:
        # Fetch N articles (you might want to add ordering/sampling logic here)
        articles_orm = session.query(FactCheckArticles).limit(num_articles).all()

        if not articles_orm:
            print("No articles found in the database. Exiting.")
            return
        
        classifier_agent = TopicClassifierAgent(model_name=model_name)
        
        for article_orm in articles_orm:
            article_id = article_orm.id
            headline = article_orm.headline if article_orm.headline else ""
            kicker = article_orm.kicker if article_orm.kicker else ""
            teaser = article_orm.teaser if article_orm.teaser else ""
            url = article_orm.url if article_orm.url else ""
            
            article_content = FactCheckArticleContent(
                kicker=kicker,
                headline=headline,
                teaser=teaser,
                body=article_orm.body if article_orm.body else []
            )

            print(f"Classifying article ID: {article_id} - Headline: {headline[:70]}...")
            
            classified_topic_label = "ERROR_CLASSIFYING_TOPIC" # Default in case of LLM failure
            try:
                classified_topic: Topic = await classifier_agent.run(article_content)
                classified_topic_label = classified_topic.topic_label
            except Exception as e:
                print(f"❌ Error classifying article {article_id}: {e}")
            
            results.append({
                "id": article_id,
                "headline": headline,
                "kicker": kicker,
                "teaser": teaser,
                "url": url,
                "topic": classified_topic_label
            })

    if results:
        df = pd.DataFrame(results)
        df.to_csv(output_csv, index=False)
        print(f"\n✅ Successfully classified {len(results)} articles and saved to {output_csv}")
    else:
        print("\nNo articles were classified.")


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description="Classify N fact-check articles using the TopicClassifierAgent and save to CSV."
    )
    parser.add_argument(
        "--num_articles",
        type=int,
        default=10,
        help="Number of articles to load and classify from the database (default: 10)."
    )
    parser.add_argument(
        "--output_csv",
        type=str,
        default="classified_articles.csv",
        help="Path to the output CSV file (default: classified_articles.csv)."
    )
    parser.add_argument(
        "--model",
        dest="model_name",
        type=str,
        default=None,
        help="Optional: Specify a different LLM model name."
    )
    
    args = parser.parse_args()
    asyncio.run(
        classify_articles_to_csv_cli(
            num_articles=args.num_articles,
            output_csv=args.output_csv,
            model_name=args.model_name
        )
    )

