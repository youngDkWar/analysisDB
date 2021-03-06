import psycopg2
import json
import time
import os
from psycopg2.extras import RealDictCursor
from dotenv import load_dotenv, dotenv_values
from django.core.serializers.json import DjangoJSONEncoder

t = time
timer = 0
load_dotenv()


def queryConstructor(data):
    """Создаёт sql запрос в виде строки по полученным фильтрам с сайта
         
    Args:
        data (dict): Json словарь полученый с фронта.

    Returns:
        str: Готовый SQL запрос.

    """
    query = ["SELECT * FROM links WHERE "]
    sql_args = []

    if data['mainfilter']['Child'] != "" and data['mainfilter']['Parent'] != "":
        sql_args.append(f'child={data["mainfilter"]["Child"]}')
        sql_args.append(f'parent={data["mainfilter"]["Parent"]}')

    elif data['mainfilter']['Parent'] != "":
        sql_args.append(f'parent={data["mainfilter"]["Parent"]}')

    elif data['mainfilter']['Child'] != "":
        sql_args.append(f'child={data["mainfilter"]["Child"]}')

    else:
        sql_args.append(f'pk=0')

    if data['kind'] != "-":
        sql_args.append(f'kind={data["kind"]}')

    if data['date_begin'] != "":
        sql_args.append(f"date_begin >= '{data['date_begin']}'")

    if data['date_end'] != "":
        sql_args.append(f"date_end <= '{data['date_end']}'")

    if data['cost'] != "":
        sql_args.append(f'cost={data["cost"]}')

    if data['share'] != "":
        sql_args.append(f'share={data["share"]}')

    if data['child_liquidated'] != "-":
        sql_args.append(f'child_liquidated={data["child_liquidated"]}')

    query.append(" AND ".join(sql_args))

    #query.append(" LIMIT 3")

    return "".join(query)


def getDataPostgreSQL(request):
    """Получает данные по запросу request из базы данных postgres и возвращает их вместе с временем,
         за которое он эти данные получил

    Args:
        request (object): Объект, в котором хранится json словарь с данными из запроса.

    Keyword Args:
        data (dict): Словарь с данными из запроса.
        to_json (dict): Хранит результат обращения к базе данных в формате json.
        
    Returns:
        json: Возвращает данные из базы PostgreSQL по запросу. 

    """

    data = request.data
    to_json = {}
    host = os.getenv('postgres_host')
    user = os.getenv('postgres_user')
    password = os.getenv('postgres_password')
    db_name = os.getenv('postgres_db_name')
    try:
        connection = psycopg2.connect(
            host=host,
            user=user,
            password=password,
            database=db_name
            )
        with connection.cursor(cursor_factory=RealDictCursor) as cursor:
            time_start = t.perf_counter()
            query = queryConstructor(data)
            cursor.execute(query)
            time_end = t.perf_counter()
            result = cursor.fetchall()
            timer = time_end - time_start
            to_json = json.dumps(
                result,
                cls=DjangoJSONEncoder)
            all_data = {"result": to_json, "nodes": [], "nodes_type": ''}
            temp = to_json.split("}")
            for i in range(len(temp) - 1):
                i1, i2 = 0, 0
                if data['mainfilter']['Child'] != "" and data['mainfilter']['Parent'] != "":
                    break
                elif data['mainfilter']['Child'] != "":
                    i1 = temp[i].find("parent") + 9
                    i2 = temp[i].find("child") - 3
                    all_data["nodes_type"] = "parent"
                elif data['mainfilter']['Parent'] != "":
                    i1 = temp[i].find("child") + 8
                    i2 = temp[i].find("kind") - 3
                    all_data["nodes_type"] = "child"
                id = temp[i][i1:i2]
                cursor.execute(f'SELECT * FROM face_info WHERE face_id={int(id)} LIMIT 1')
                node = cursor.fetchall()
                json_node = json.dumps(node)
                all_data["nodes"].append(json_node)

    except Exception as _ex:
        print("Error : ", _ex)
    finally:
        if connection:
            connection.close()
            print("connection closed")

    all_data['result'] += str(timer)

    return all_data
