import psycopg2
import json
from psycopg2.extras import RealDictCursor


def getDataPostgreSQL(request):
    host = "127.0.0.1"
    user = "postgres"
    password = "postgres"
    db_name = "links"
    try:
        connection = psycopg2.connect(
            host=host,
            user=user,
            password=password,
            database=db_name
            )
        with connection.cursor(cursor_factory=RealDictCursor) as cursor:
            cursor.execute("SELECT * FROM links WHERE pk='1'")
            result = cursor.fetchall()
            for record in result:
                print(record)
                print(result)
            to_json = json.dumps(result)
            print(to_json)
    except Exception as _ex:
        print("Error : ", _ex)
    finally:
        if connection:
            connection.close()
            print("connection closed")
    return to_json