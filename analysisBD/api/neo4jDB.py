import neo4j
import time

from neo4j import GraphDatabase, basic_auth

t = time

connection = GraphDatabase.driver(
        "bolt://localhost:5332",
        auth=basic_auth("neo4j", "12345678"))

"""
connection = GraphDatabase.driver(
        "bolt://46.48.3.74:5332",
        auth=basic_auth("neo4j", "12345678"))
"""


def getDataNeo4j(request):
    cypher_query = '''
    match (n) return n LIMIT 25;
    '''
    """
    # match ()-[r]->() return count(r);
    # match (r) return count(r);
    def get_node_tx(tx, name):
        time_start = t.perf_counter()
        result = tx.run(cypher_query, name=name)
        time_end = t.perf_counter()
        value = result.data()
        timer = time_end - time_start
        return value, timer
    """
    with connection.session(database="neo4j") as session:
        results = session.run(cypher_query)
        #result_json = {results.data()[0]}
        return results.data()


    #results.append({'time': timer, 'name': "time"})

     #{1: "Neo4j", 2: "тест"}   Это обязательно JSON


def createTestDataNe04j(request):
    driver = connection

    def create_node_tx(tx, name):
        time_start = t.perf_counter()
        for i in range(int(10)):
            tx.run("CREATE (ee:Person {name: 'Emil', from: 'Sweden', kloutScore: " + str(i) + "})", name=name)
        time_end = t.perf_counter()
        return time_end - time_start

    with driver.session(database="neo4j") as session:
        results = session.write_transaction(create_node_tx, "name")

    driver.close()

    return results

#getDataNeo4j("")
#connection.close()