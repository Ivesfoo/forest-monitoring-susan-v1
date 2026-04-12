from database.connection import get_connection


def initialize_database():
    conn = get_connection()
    cursor = conn.cursor()

    with open("database/schema.sql", "r", encoding="utf-8") as f:
        schema_sql = f.read()

    cursor.executescript(schema_sql)
    conn.commit()
    conn.close()

    print("Database initialized successfully.")


if __name__ == "__main__":
    initialize_database()