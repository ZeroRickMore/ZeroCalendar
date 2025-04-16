import sqlite3, os, pprint

if __name__ == '__main__':

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