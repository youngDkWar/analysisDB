from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.decorators import api_view
from . import neo4jDB, orientdb, postgresql, controller


def hello(request):
    return render(request, 'index.html')


def deep(request):
    return render(request, 'deepData.html')


def orient(request):
    return render(request, 'orientdb.html')


def postgre(request):
    return render(request, 'postgresql.html')


def Neo4j(request):
    return render(request, 'neo4j.html')


@api_view(['GET'])
def getNeo4jData(request):
    return Response(data=neo4jDB.getDataNeo4j(request), status=200)


@api_view(['GET'])
def createNeo4jTestData(request):
    return Response(data=neo4jDB.createTestDataNe04j(request), status=200)


@api_view(['GET'])
def getOrientDBData(request):
    return Response(data=orientdb.getDataOrientDB(request), status=200)


@api_view(['POST'])
def getPostgreSQLData(request):
    return Response(data=postgresql.getDataPostgreSQL(request), status=200)


@api_view(['POST'])
def getData(request):
    return Response(data=controller.getData(request), status=200)


@api_view(['POST'])
def getDeepData(request):
    return Response(data=controller.getDeepData(request), status=200)
