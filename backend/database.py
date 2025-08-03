import sys
from pathlib import Path

project_root = str(Path(__file__).parent)
sys.path.append(project_root)

from contextlib import contextmanager
from typing import Generator
from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker
from models import Base
import os
from dotenv import load_dotenv


class Database:
    '''
    Database connection manager that handles SQLAlchemy session lifecycle.
    
    Exposes a context manager for handling database sessions with automatic commit/rollback
    and cleanup.
    '''
    def __init__(self):
        load_dotenv()
        self.connection_string = os.getenv('DATABASE_URL')
        if not self.connection_string:
            raise ValueError('DATABASE_URL not found in environment variables')
        self.engine = create_engine(self.connection_string)
        self.Session = sessionmaker(bind=self.engine)
    
    def init_db(self):
        Base.metadata.create_all(self.engine)
    
    @contextmanager
    def get_session(self) -> Generator[Session, None, None]:
        session = self.Session()
        try:
            yield session
            session.commit()
        except Exception:
            session.rollback()
            raise
        finally:
            session.close() 