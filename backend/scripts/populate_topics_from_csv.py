import sys
from pathlib import Path
import pandas as pd

# Add the Python project root to sys.path
python_project_root = Path(__file__).resolve().parent.parent # Points to /backend/
if str(python_project_root) not in sys.path:
    sys.path.insert(0, str(python_project_root))

from shared.database import Database
from shared.services.fact_check_articles_service import FactCheckArticlesService

def populate_topics_from_csv(csv_file: str = "topic_classification_test.csv"):
    """
    Read topics from a CSV file and populate the topic column in the database.
    Only updates articles that have a topic assigned in the CSV.
    """
    # Check if CSV file exists
    if not Path(csv_file).exists():
        print(f"Error: CSV file '{csv_file}' not found.")
        return
    
    print(f"Reading topics from {csv_file}...")
    df = pd.read_csv(csv_file)
    
    # Ensure required columns exist
    if 'id' not in df.columns or 'topic' not in df.columns:
        print("Error: CSV must contain 'id' and 'topic' columns.")
        return
    
    # Filter for rows with non-null topics
    df_with_topics = df[df['topic'].notna()].copy()
    
    if df_with_topics.empty:
        print("No topics found in the CSV file.")
        return
    
    print(f"Found {len(df_with_topics)} articles with topics to update.")
    
    db_instance = Database()
    updated_count = 0
    error_count = 0
    
    with db_instance.get_session() as db:
        service = FactCheckArticlesService(db)
        
        for idx, row in df_with_topics.iterrows():
            article_id = row['id']
            topic = row['topic']
            
            try:
                # Update the article with the topic
                service.update_article(article_id, {'topic': topic})
                updated_count += 1
                
                if (updated_count % 10) == 0:
                    print(f"  Updated {updated_count} articles...")
                    
            except Exception as e:
                print(f"  Error updating article {article_id}: {e}")
                error_count += 1
    
    print(f"\n✅ Successfully updated {updated_count} articles.")
    if error_count > 0:
        print(f"❌ Failed to update {error_count} articles.")


if __name__ == '__main__':
    import argparse
    
    parser = argparse.ArgumentParser(
        description="Populate the topic column in the database from a CSV file."
    )
    parser.add_argument(
        "--csv",
        type=str,
        default="topic_classification_test.csv",
        help="Path to the CSV file containing topics (default: topic_classification_test.csv)."
    )
    
    args = parser.parse_args()
    populate_topics_from_csv(csv_file=args.csv)

