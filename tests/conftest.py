import pytest
import sqlite3
import os

@pytest.fixture
def db_connection():
    # Path to test database
    db_path = os.path.join(os.path.dirname(__file__), 'test_data.db')
    
    # Create connection
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row # Allows accessing columns by name
    
    yield conn
    
    # Cleanup
    conn.close()