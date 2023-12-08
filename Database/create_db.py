from psycopg2 import connect, OperationalError, sql, DatabaseError

try:
    cnx = connect(
        user='postgres',
        password='coderslab',
        host='localhost',
        port='5433',
        database='postgres'
    )

    cursor = cnx.cursor()
    print('Connected')
except OperationalError as err:
    print('Connection error')
    raise ValueError(f'Connection error: {err}')