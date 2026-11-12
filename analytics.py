
import sqlite3
from pathlib import Path


def run_sql_queries(
    db_path="data/solarwatch.db",
    sql_path="sql/queries.sql"
):
    connection = sqlite3.connect(db_path)

    try:
        sql_file = Path(sql_path)
        sql_content = sql_file.read_text(encoding="utf-8")

        cursor = connection.cursor()

        queries = [
            query.strip()
            for query in sql_content.split(";")
            if query.strip()
        ]

        for number, query in enumerate(queries, start=1):
            cursor.execute(query)

            if cursor.description is None:
                continue

            columns = [
                description[0]
                for description in cursor.description
            ]

            rows = cursor.fetchall()

            print(f"\nQUERY {number}")
            print("-" * 50)
            print(" | ".join(columns))

            for row in rows:
                print(" | ".join(str(value) for value in row))

    finally:
        connection.close()


if __name__ == "__main__":
    run_sql_queries()
