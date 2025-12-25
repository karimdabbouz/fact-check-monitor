import sys, asyncio
from pathlib import Path
from typing import List, Optional, Dict, Any
import pandas as pd
import math
import os

project_root = str(Path(__file__).parent.parent)
sys.path.append(str(project_root))

from shared.schemas import FactCheckArticleContent, FactCheckArticlesSchema, LLMGeneratedTopic
from shared.agents.topic_generator import TopicGeneratorAgent
from shared.database import Database
from shared.services.fact_check_articles_service import FactCheckArticlesService
from shared.models import FactCheckArticles # Import the SQLAlchemy model

async def generate_topics_for_sample(sample_size: int = 100):
    """
    Generates topics for a sample of articles, evenly distributed by medium and published_at,
    and stores the results in a local CSV file, avoiding articles already processed.
    """
    db = Database()
    topic_generator = TopicGeneratorAgent(
        # model_name='mistralai/devstral-2512:free' # Or your preferred model
        model_name='anthropic/claude-haiku-4.5'
    )
    output_file = "llm_generated_topics_sample.csv"
    existing_processed_ids = set()
    existing_df = pd.DataFrame()
    
    # Load existing CSV if it exists to get already processed article IDs
    if os.path.exists(output_file):
        try:
            existing_df = pd.read_csv(output_file)
            existing_processed_ids = set(existing_df['id'].tolist())
            print(f"Loaded {len(existing_processed_ids)} previously processed articles from {output_file}.")
        except pd.errors.EmptyDataError:
            print(f"Existing CSV file {output_file} is empty or has no data. Starting fresh.")
            existing_df = pd.DataFrame(columns=['id', 'medium', 'url', 'headline', 'kicker', 'teaser', 'llm_topic'])
        except Exception as e:
            print(f"Error loading existing CSV file {output_file}: {e}. Starting fresh.")
            existing_df = pd.DataFrame(columns=['id', 'medium', 'url', 'headline', 'kicker', 'teaser', 'llm_topic'])

    results_to_append = []

    with db.get_session() as session:
        service = FactCheckArticlesService(session)

        # Get all distinct mediums
        mediums = [result[0] for result in session.query(FactCheckArticles.medium).distinct().all()]
        if not mediums:
            print("No mediums found in the database. Exiting.")
            return

        # Calculate sample size per medium
        num_mediums = len(mediums)
        articles_per_medium_target = math.ceil(sample_size / num_mediums)

        for medium in mediums:
            # Get articles for the current medium, ordered by published_at for even distribution
            # Exclude already processed articles
            medium_articles_query = session.query(FactCheckArticles).filter(FactCheckArticles.medium == medium)
            if existing_processed_ids:
                medium_articles_query = medium_articles_query.filter(~FactCheckArticles.id.in_(existing_processed_ids))
            
            medium_articles = medium_articles_query.order_by(FactCheckArticles.published_at).all()

            if not medium_articles:
                print(f"No new articles found for medium: {medium}")
                continue

            # Take an evenly distributed sample from this medium's articles
            actual_sample_size_for_medium = min(articles_per_medium_target, len(medium_articles))
            
            if actual_sample_size_for_medium > 0:
                indices = [int(i * (len(medium_articles) / actual_sample_size_for_medium)) for i in range(actual_sample_size_for_medium)]
                sampled_articles = [medium_articles[i] for i in indices]
            else:
                sampled_articles = []
            
            print(f"Processing {len(sampled_articles)} new articles for medium: {medium}")

            for article_orm in sampled_articles:
                article = FactCheckArticlesSchema.model_validate(article_orm.__dict__)

                # Handle potential None values for article fields
                article_id = article.id
                medium = article.medium
                url = article.url
                headline = article.headline if article.headline is not None else "N/A"
                kicker = article.kicker if article.kicker is not None else "N/A"
                teaser = article.teaser if article.teaser is not None else "N/A"
                body = article.body # body is a List[BodyBlock], so it should be safe even if empty

                article_content = FactCheckArticleContent(
                    kicker=kicker,
                    headline=headline,
                    teaser=teaser,
                    body=body
                )

                print(f"Generating topic for article ID: {article_id} - Headline: {headline[:50]}...")
                
                topic_label = "ERROR_GENERATING_TOPIC" # Default in case of LLM failure

                try:
                    generated_topic: LLMGeneratedTopic = await topic_generator.run(article_content)
                    topic_label = generated_topic.topic_label
                except Exception as e:
                    print(f"Error generating topic for article {article_id}: {e}")

                results_to_append.append({
                    'id': article_id,
                    'medium': medium,
                    'url': url,
                    'headline': headline,
                    'kicker': kicker,
                    'teaser': teaser,
                    'llm_topic': topic_label
                })
                # Pause to respect API rate limits if needed (e.g., time.sleep(1))
    
    if results_to_append:
        new_df = pd.DataFrame(results_to_append)
        if not existing_df.empty:
            final_df = pd.concat([existing_df, new_df], ignore_index=True)
        else:
            final_df = new_df
        
        final_df.to_csv(output_file, index=False)
        print(f"Successfully generated topics for {len(results_to_append)} new articles and updated {output_file}")
    else:
        print("No new topics generated.")


if __name__ == '__main__':
    asyncio.run(generate_topics_for_sample(sample_size=30))