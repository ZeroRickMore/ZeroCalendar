import sqlite3

if __name__ == '__main__':

    while True:
        conn = sqlite3.connect('sqlite.db')
        c = conn.cursor()
        query = input("Query -> ")

        if query == 'EXIT':
            break

        c.execute(query)
        rows = c.fetchall()

        print("\nRESULT:\n\n---\n", rows, "\n---\n\n")

        conn.commit()
        conn.close()

    print("\n\nGoodbye!\n")