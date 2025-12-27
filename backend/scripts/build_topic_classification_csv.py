import sys, asyncio
from pathlib import Path
from typing import Optional, Set
import argparse
import pandas as pd
import os
import json

# Add the Python project root to sys.path
python_project_root = Path(__file__).resolve().parent.parent # Points to /backend/
if str(python_project_root) not in sys.path:
    sys.path.insert(0, str(python_project_root))

from shared.database import Database
from shared.models import FactCheckArticles
from shared.schemas import FactCheckArticleContent, Topic
from shared.agents.topic_classifier import TopicClassifierAgent

async def build_topic_classification_csv(num_articles: int, csv_file: str = "topic_classification_test.csv", model_name: Optional[str] = None):
    """
    Build or append to a CSV file with all database columns plus classified topics.
    
    - If CSV exists: Load it, find articles not yet classified, and add up to num_articles new articles.
    - If CSV doesn't exist: Fetch and classify num_articles from the database.
    
    This creates a complete mirror of the database with all columns (including JSONB fields)
    that can be used for Streamlit visualization and experimentation.
    """
    db = Database()
    
    # Load existing CSV if it exists
    existing_ids: Set[int] = set()
    existing_df = pd.DataFrame()
    
    if os.path.exists(csv_file):
        print(f"Loading existing CSV file: {csv_file}")
        existing_df = pd.read_csv(csv_file)
        existing_ids = set(existing_df['id'].tolist())
        print(f"Found {len(existing_ids)} articles already classified in {csv_file}.")
    else:
        print(f"CSV file {csv_file} does not exist. Creating a new one.")
    
    # Fetch articles from DB and filter out those already in the CSV
    print(f"Fetching articles from the database...")
    with db.get_session() as session:
        # Get all articles, ordered by ID
        all_articles_orm = session.query(FactCheckArticles).order_by(FactCheckArticles.id).all()
        
        # Filter out articles already in the CSV
        articles_to_classify = [
            article for article in all_articles_orm 
            if article.id not in existing_ids
        ]
        
        if not articles_to_classify:
            print(f"✅ All {len(existing_ids)} articles in the database are already classified in {csv_file}.")
            return
        
        # Take only the first num_articles from the unclassified ones
        articles_to_classify = articles_to_classify[:num_articles]
        
        print(f"Found {len(articles_to_classify)} new articles to classify (requesting {num_articles}).")
        
        classifier_agent = TopicClassifierAgent(model_name=model_name)
        new_results = []
        
        for idx, article_orm in enumerate(articles_to_classify, 1):
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

            print(f"[{idx}/{len(articles_to_classify)}] Classifying article ID: {article_id} - Headline: {headline[:60]}...")
            
            classified_topic_label = "ERROR_CLASSIFYING_TOPIC" # Default in case of LLM failure
            try:
                classified_topic: Topic = await classifier_agent.run(article_content)
                classified_topic_label = classified_topic.topic_label
            except Exception as e:
                print(f"  ❌ Error classifying article {article_id}: {e}")
            
            # Extract all columns from the article ORM object
            new_results.append({
                "id": article_orm.id,
                "url": article_orm.url,
                "medium": article_orm.medium,
                "category": article_orm.category,
                "author": article_orm.author,
                "kicker": article_orm.kicker,
                "headline": article_orm.headline,
                "teaser": article_orm.teaser,
                "body": json.dumps(article_orm.body) if article_orm.body else None,  # Serialize JSONB to string
                "image_url": article_orm.image_url,
                "published_at": article_orm.published_at,
                "topic": classified_topic_label,
                "claim": article_orm.claim,
                "instrumentalizer": article_orm.instrumentalizer,
                "entities": json.dumps(article_orm.entities) if article_orm.entities else None,  # Serialize JSONB to string
                "last_updated": article_orm.last_updated
            })
        
        # Combine with existing data and save
        if new_results:
            new_df = pd.DataFrame(new_results)
            
            if not existing_df.empty:
                combined_df = pd.concat([existing_df, new_df], ignore_index=True)
            else:
                combined_df = new_df
            
            combined_df.to_csv(csv_file, index=False)
            print(f"\n✅ Successfully classified {len(new_results)} new articles.")
            print(f"✅ Total articles in {csv_file}: {len(combined_df)}")
            print(f"✅ Exported all database columns to CSV.")
        else:
            print("\nNo new articles were classified.")


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description="Build or append to a CSV file with all database columns plus classified topics. Incremental classification ensures no duplicates."
    )
    parser.add_argument(
        "--num_articles",
        type=int,
        default=10,
        help="Number of new (unclassified) articles to fetch and classify (default: 10)."
    )
    parser.add_argument(
        "--csv",
        dest="csv_file",
        type=str,
        default="topic_classification_test.csv",
        help="Path to the CSV file (default: topic_classification_test.csv)."
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
        build_topic_classification_csv(
            num_articles=args.num_articles,
            csv_file=args.csv_file,
            model_name=args.model_name
        )
    )
