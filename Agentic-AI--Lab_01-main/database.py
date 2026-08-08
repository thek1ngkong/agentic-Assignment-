import sqlite3
import os

DB_NAME = "college.db"

def get_db_path():
    return os.path.join(os.path.dirname(__file__), DB_NAME)

def get_db_connection():
    conn = sqlite3.connect(get_db_path())
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    """Creates the students table and inserts 10 sample records if the table is empty."""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # Create table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS students (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            department TEXT NOT NULL,
            marks INTEGER NOT NULL
        )
    ''')
    
    # Check if table already has records
    cursor.execute('SELECT COUNT(*) FROM students')
    count = cursor.fetchone()[0]
    
    if count == 0:
        sample_students = [
            ('Alice Johnson', 'Computer Science', 85),
            ('Bob Smith', 'Mechanical Engineering', 72),
            ('Charlie Brown', 'Electronics', 90),
            ('Diana Prince', 'Computer Science', 94),
            ('Evan Wright', 'Electrical Engineering', 65),
            ('Fiona Gallagher', 'Civil Engineering', 81),
            ('George Clark', 'Computer Science', 78),
            ('Hannah Abbott', 'Electronics', 88),
            ('Ian Malcolm', 'Mechanical Engineering', 92),
            ('Julia Roberts', 'Civil Engineering', 69)
        ]
        cursor.executemany('''
            INSERT INTO students (name, department, marks)
            VALUES (?, ?, ?)
        ''', sample_students)
        conn.commit()
    
    conn.close()

def get_schema():
    """Returns the database schema description to pass to the LLM."""
    return """CREATE TABLE students (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    department TEXT NOT NULL,
    marks INTEGER NOT NULL
);"""

def execute_query(sql_query):
    """
    Executes the generated SQL query safely on SQLite and returns columns and row data.
    """
    clean_sql = sql_query.strip().strip(';').strip()
    
    # Safety verification: ensure only read-only SELECT queries run in lab context
    upper_sql = clean_sql.upper()
    if not (upper_sql.startswith("SELECT") or upper_sql.startswith("WITH")):
        raise ValueError("Security constraint: Only SELECT queries are permitted.")
        
    forbidden = ["DROP", "DELETE", "UPDATE", "INSERT", "ALTER", "TRUNCATE", "CREATE", "EXEC"]
    for keyword in forbidden:
        if f" {keyword} " in f" {upper_sql} ":
            raise ValueError(f"Security constraint: Query contains restricted operation '{keyword}'.")
            
    conn = get_db_connection()
    cursor = conn.cursor()
    
    cursor.execute(sql_query)
    rows = cursor.fetchall()
    
    columns = [desc[0] for desc in cursor.description] if cursor.description else []
    results = [dict(row) for row in rows]
    
    conn.close()
    return columns, results

if __name__ == "__main__":
    init_db()
    print("Database initialized successfully with sample data.")
    print("Schema:\n" + get_schema())
