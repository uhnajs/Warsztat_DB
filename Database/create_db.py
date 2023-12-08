from psycopg2 import connect, OperationalError, errors, sql


db_connector = {
    'user': 'postgres',
    'password': 'coderslab',
    'host': 'localhost',
    'port': '5433',
    'database': 'exercise_db'
}
def create_database():
    try:
        # Używamy **db_connector do rozpakowania słownika jako argumentów nazwanych
        cnx = connect(**db_connector)
        cnx.autocommit = True
        with cnx.cursor() as cursor:
            cursor.execute("CREATE DATABASE exercise_db;")
            print("Database 'exercise_db' has been created.")
        cnx.close()
    except errors.DuplicateDatabase:
        print("Database 'exercise_db' already exists.")
    except OperationalError as err:
        print(f'Connection error while creating database: {err}')
        raise

def create_users_table():
    try:
        with connect(**db_connector) as cnx:
            cnx.autocommit = True
            with cnx.cursor() as cursor:
                create_table_query = sql.SQL("""
                    CREATE TABLE IF NOT EXISTS users (
                        id SERIAL PRIMARY KEY,
                        username VARCHAR(255),
                        hashed_password VARCHAR(80)
                    );
                """)
                cursor.execute(create_table_query)
                print("Table 'users' has been created or already exists.")
    except OperationalError as err:
        print(f'Connection error while creating table: {err}')
        raise

def create_messages_table():
    try:
        with connect(**db_connector) as cnx:
            cnx.autocommit = True
            with cnx.cursor() as cursor:
                create_table_query = sql.SQL("""
                    CREATE TABLE IF NOT EXISTS messages (
                        id SERIAL PRIMARY KEY,
                        from_id INTEGER REFERENCES users(id),
                        to_id INTEGER REFERENCES users(id),
                        creation_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                        text VARCHAR(255)
                    );
                """)
                cursor.execute(create_table_query)
                print("Table 'messages' has been created or already exists.")
    except OperationalError as err:
        print(f"Connection error while creating the 'messages' table: {err}")
        raise

def main():
    create_database()
    create_users_table()
    create_messages_table()

if __name__ == "__main__":
    main()