import sys
from pathlib import Path
from typing import List, Optional, Dict, Any

project_root = str(Path(__file__).parent.parent)
sys.path.append(str(project_root))

from shared.schemas import FactCheckArticleContent, FactCheckArticlesSchema, LLMGeneratedTopic
from shared.agents.topic_generator import TopicGeneratorAgent
from shared.database import Database
from shared.services.fact_check_articles_service import FactCheckArticlesService


def get_llm_topic_for_article(article_id: int):
    """
    Fetches an article by ID, assembles its content, sends to LLM to get a topic,
    and updates the article with the generated topic.
    """
    db = Database()
    with db.get_session() as session:
        service = FactCheckArticlesService(session)
        article: FactCheckArticlesSchema = service.get_article(article_id=article_id)

        if not article:
            print(f"Article with ID {article_id} not found.")
            return

        article_content = FactCheckArticleContent(
            kicker=article.kicker,
            headline=article.headline,
            teaser=article.teaser,
            body=article.body
        )

        topic_generator = TopicGeneratorAgent(
            model_name='anthropic/claude-haiku-4.5'
        )

        print(f"Generating topic for article ID: {article_id} - Headline: {article.headline}")
        generated_topic: LLMGeneratedTopic = topic_generator.run(article_content) # Assuming agent.run now takes FactCheckArticleContent

        print(f"Generated Topic: {generated_topic.topic_label}")

        # Update the article in the database with the generated topic
        service.update_article(
            article_id=article_id,
            update_data={'llm_generated_topic': generated_topic.topic_label}
        )
        print(f"Article {article_id} updated with topic: {generated_topic.topic_label}")


if __name__ == '__main__':
    # Example usage: Generate topic for article with ID 2
    get_llm_topic_for_article(article_id=2)
