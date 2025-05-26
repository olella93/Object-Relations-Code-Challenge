import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))


from lib.db.connection import get_connection

if __name__ == '__main__':
    conn = get_connection()
    with open('lib/db/schema.sql') as f:
        conn.executescript(f.read())
    conn.commit()
    conn.close()
    print("Database initialized.")