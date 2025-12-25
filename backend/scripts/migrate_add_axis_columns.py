"""
Migration script to update the fact_check_articles table schema.
This script:
1. Drops the llm_generated_topic column (no longer needed)
2. Adds new axis columns (claim, instrumentalizer, entities)

All existing data is preserved during this migration.

Run this script once to apply the migration.
"""

import sys
from pathlib import Path

project_root = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(project_root))

from sqlalchemy import text
from backend.shared.database import Database


def migrate_schema():
    """
    Update the fact_check_articles table schema:
    - Remove llm_generated_topic (no longer used)
    - Add claim, instrumentalizer, and entities columns
    
    This is a safe migration that preserves all existing data.
    """
    db = Database()
    
    # SQL statements to update the schema
    migration_statements = [
        # Drop llm_generated_topic column if it exists
        """
        ALTER TABLE fact_check_articles
        DROP COLUMN IF EXISTS llm_generated_topic;
        """,
        # Add claim column (Axis 2)
        """
        ALTER TABLE fact_check_articles
        ADD COLUMN IF NOT EXISTS claim TEXT;
        """,
        # Add instrumentalizer column (Axis 3)
        """
        ALTER TABLE fact_check_articles
        ADD COLUMN IF NOT EXISTS instrumentalizer TEXT;
        """,
        # Add entities column (Axis 4) as JSONB for storing list of entities
        """
        ALTER TABLE fact_check_articles
        ADD COLUMN IF NOT EXISTS entities JSONB;
        """,
    ]
    
    try:
        with db.engine.connect() as connection:
            for statement in migration_statements:
                print(f"Executing: {statement.strip()[:60]}...")
                connection.execute(text(statement))
                connection.commit()
        
        print("\n✅ Migration successful!")
        print("   Removed: llm_generated_topic")
        print("   Added:   claim (TEXT)")
        print("   Added:   instrumentalizer (TEXT)")
        print("   Added:   entities (JSONB)")
        
    except Exception as e:
        print(f"❌ Migration failed: {e}")
        raise


if __name__ == '__main__':
    print("Starting schema migration...")
    print("=" * 60)
    migrate_schema()
    print("=" * 60)

