import sqlite3

# Connect to DB
conn = sqlite3.connect("ecpm.db")
cursor = conn.cursor()

# List all tables
cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
tables = cursor.fetchall()

print("Tables in database:")
for table in tables:
    table_name = table[0]
    print(f"- {table_name}")
    
    # Get columns in each table
    cursor.execute(f"PRAGMA table_info({table_name})")
    columns = cursor.fetchall()
    print("  Columns:")
    for col in columns:
        print(f"   - {col[1]}")

conn.close()
