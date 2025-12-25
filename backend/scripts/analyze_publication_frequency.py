import sys
from pathlib import Path
import pandas as pd
import argparse
from datetime import datetime, timedelta

# Add project root to sys.path to allow absolute imports
project_root = str(Path(__file__).parent.parent)
sys.path.append(project_root)

from shared.database import Database
from shared.models import FactCheckArticles
from sqlalchemy import func

def parse_date(date_string):
    try:
        return datetime.strptime(date_string, '%Y-%m-%d').date()
    except ValueError:
        raise argparse.ArgumentTypeError("Date must be in YYYY-MM-DD format.")

def analyze_publication_frequency_cli(date: str = None, interval: str = 'week', medium: str = None):
    """
    Connects to the database and prints statistics on the number of articles published.
    Allows filtering by date, interval (day, week, month), and medium.
    """
    db = Database()
    
    print(f"Connecting to database and fetching articles for '{interval}' interval...")
    with db.get_session() as session:
        query = session.query(FactCheckArticles)

        if medium:
            query = query.filter(FactCheckArticles.medium == medium)

        articles = query.all()
        
        articles_data = []
        for article in articles:
            if article.published_at:
                articles_data.append({
                    'published_at': article.published_at,
                    'medium': article.medium # Include medium for later filtering
                })

    if not articles_data:
        print("No articles found or no publication dates available for the given criteria.")
        return

    df = pd.DataFrame(articles_data)
    df['published_at'] = pd.to_datetime(df['published_at'])
    
    # Filter by a specific date if provided
    if date:
        target_date = datetime.strptime(date, '%Y-%m-%d').date()
        df = df[df['published_at'].dt.date == target_date]
        if df.empty:
            print(f"No articles found for {date}.")
            return

    # Determine grouping frequency based on interval
    if interval == 'day':
        grouping_key = df['published_at'].dt.date
        print(f"\n--- Articles Published on {date if date else 'Each Day'} ---")
    elif interval == 'week':
        grouping_key = df['published_at'].dt.to_period('W')
        print(f"\n--- Articles Published per Week (for {date if date else 'All Weeks'}) ---")
    elif interval == 'month':
        grouping_key = df['published_at'].dt.to_period('M')
        print(f"\n--- Articles Published per Month (for {date if date else 'All Months'}) ---")
    else:
        print("Invalid interval. Please choose 'day', 'week', or 'month'.")
        return

    # Group and count articles
    if medium:
        # If a specific medium is requested, just show counts for that medium
        result = df.groupby(grouping_key).size()
        print(f"Total articles for medium '{medium}': {result.sum()}")
    else:
        # Show total counts and breakdown by medium
        total_counts = df.groupby(grouping_key).size()
        print(f"Total articles in selected interval(s): {total_counts.sum()}")
        print("\nBreakdown by Medium:")
        medium_counts = df.groupby([grouping_key, df['medium']]).size().unstack(fill_value=0)
        print(medium_counts.sort_index(ascending=False).to_string())
        print("\nTotal per interval:")
        print(total_counts.sort_index(ascending=False).to_string())

    print("\nAnalysis complete.")

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Analyze article publication frequency.')
    parser.add_argument('--date', type=str, help='Specific date (YYYY-MM-DD) to filter results. Only applicable with --interval day.')
    parser.add_argument('--interval', type=str, choices=['day', 'week', 'month'], default='week', 
                        help='Interval for aggregation: day, week, or month. Default is \'week\'.')
    parser.add_argument('--medium', type=str, help='Filter by specific publication medium (e.g., tagesschau-faktenfinder).')

    args = parser.parse_args()

    if args.date and args.interval != 'day':
        parser.error("--date can only be used with --interval day.")
    
    analyze_publication_frequency_cli(date=args.date, interval=args.interval, medium=args.medium)