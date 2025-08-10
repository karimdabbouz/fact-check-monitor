import sys
from pathlib import Path

project_root = str(Path(__file__).parent.parent)
sys.path.append(str(project_root))

from shared.database import Database
from shared.services.fact_check_articles_service import FactCheckArticlesService

# --- CONFIG ---
MEDIUM = 'br-faktenfuchs'  # Set this to the medium you want to check
MIN_BODY_LENGTH = 1000  # Minimum number of characters for a 'good' body


def main():
    db = Database()
    with db.get_session() as session:
        service = FactCheckArticlesService(session)
        articles = service.get_articles(medium=MEDIUM, limit=10000)
        missing_headline = [a for a in articles if not getattr(a, 'headline', None)]
        missing_body = [a for a in articles if not getattr(a, 'body', None)]
        short_body = [a for a in articles if a.body and hasattr(a.body, '__len__') and len(str(a.body)) < MIN_BODY_LENGTH]

        print(f"Total articles for medium '{MEDIUM}': {len(articles)}")
        print(f"Articles missing headline: {len(missing_headline)}")
        print(f"Articles missing body: {len(missing_body)}")
        print(f"Articles with short body (<{MIN_BODY_LENGTH} chars): {len(short_body)}")
        if short_body:
            print("Sample short bodies:")
            for a in short_body[:5]:
                print(f"ID: {a.id}, Headline: {a.headline}, Body: {str(a.body)[:80]}...")

if __name__ == "__main__":
    main() 