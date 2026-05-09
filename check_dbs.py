import sqlite3
import os

dbs = {
    'news.db': 'data/news.db',
    'market.db': 'data/market.db',
    'gti.db': 'data/gti.db',
    'predictions.db': 'data/predictions.db'
}

for name, path in dbs.items():
    if not os.path.exists(path):
        print(f"{name}: FILE NOT FOUND")
        continue
    try:
        conn = sqlite3.connect(path)
        cursor = conn.cursor()
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        tables = cursor.fetchall()
        if tables:
            print(f"\n{name}: Tables found:")
            for table in tables:
                cursor.execute(f"SELECT COUNT(*) FROM [{table[0]}]")
                count = cursor.fetchone()[0]
                print(f"  - {table[0]}: {count} rows")
        else:
            print(f"{name}: No tables found")
        conn.close()
    except Exception as e:
        print(f"{name}: ERROR - {str(e)}")
