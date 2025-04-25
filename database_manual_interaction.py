import sqlite3, os, pprint
import sys

TABLES = ['day_events']

def flush():
    res = input("\n] FLUSHING ALL DB. ARE YOU SURE? (y) -> ")
    if res != 'y':
        sys.exit("\n] OK!! NOT FLUSHING.\n\tPhew, that was close...\n")
    print("\n] OK! FLUSHING THEN, GOODBYE DB!\n")
    for table in TABLES:
        conn = sqlite3.connect(os.path.join('instance', 'sqlite.db'))
        c = conn.cursor()
        c.execute(f"DELETE FROM {table}")
        conn.commit()
        conn.close()
        print(f"\t]- {table} flushed.")
    
    sys.exit("\n] ALL FLUSHED, BYE!\n")


if __name__ == '__main__':

    if len(sys.argv) == 2:
        arg = sys.argv[1]
        
        if arg == 'flush':
            flush()
            
    while True:
        conn = sqlite3.connect(os.path.join('instance', 'sqlite.db'))
        c = conn.cursor()
        query = input("Query -> ")

        if query == 'EXIT':
            break

        try:
            c.execute(query)
        except Exception as e:
            print(f"\n---\n\n ]ERROR : {e}\n\n---\n")
            continue

        rows = c.fetchall()

        print(f"\n---\n")
        pprint.pprint(rows)
        print("\n---\n\n")

        conn.commit()
        conn.close()

    print("\n\nGoodbye!\n")

