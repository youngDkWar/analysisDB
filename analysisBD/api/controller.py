from django.core.serializers.json import DjangoJSONEncoder
from . import neo4jDB, orientdb, postgresql


def getData(request):
    if request.data['dbtype'] == "PostgreSQL":
        return postgresql.getDataPostgreSQL(request)
    elif request.data['dbtype'] == "OrientDB":
        return orientdb.getDataOrientDB(request)
    elif request.data['dbtype'] == "Neo4j":
        return neo4jDB.getDataNeo4j(request)


def getDeepData(request):
    if request.data['dbtype'] == "PostgreSQL":
        return postgresql.colenoSQL(request)
    elif request.data['dbtype'] == "OrientDB":
        return orientdb.getDeepSearchResult(request)
    elif request.data['dbtype'] == "Neo4j":
        return neo4jDB.getGraphDataNeo4j(request)
