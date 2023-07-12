import io

from django.http import HttpResponse
from django.shortcuts import render
from django.contrib.auth.models import User
from rest_framework import viewsets
from rest_framework import permissions
from rest_framework.decorators import api_view, action
from rest_framework.parsers import JSONParser
from rest_framework.renderers import JSONRenderer
from rest_framework.response import Response

from demo.serializers import UserSerializer, DynamicTableSerializer
from .db_service import create_test_model, delete_test_model, create_model, delete_model, get_rows, add_row


# Create your views here.


class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]


class TestViewSet(viewsets.ViewSet):
    def list(self, response):
        return Response('Helo world')

    def create(self, request):
        create_test_model()
        return Response("OK")

    def destroy(self, request, pk):
        delete_test_model()
        return Response("OK")


class TableViewSet(viewsets.ViewSet):
    def list(self, response):
        return Response('XXX')

    def create(self, request):
        print(request.body)
        json_data = request.body
        stream = io.BytesIO(json_data)
        python_data = JSONParser().parse(stream)
        serializer = DynamicTableSerializer(data=python_data)
        if not serializer.is_valid():
            json_data = JSONRenderer().render(serializer.errors)
            return HttpResponse(
                json_data, content_type='application/json'
            )
        print(serializer.validated_data)
        print(serializer.data)
        create_model(serializer.data)
        return Response("OK")

    def destroy(self, request, pk):
        delete_model(pk)
        return Response("OK")

    @action(methods=['get'], detail=True)
    def rows(self, request, pk):
        all_rows = get_rows(pk)
        print(all_rows)
        json_data = JSONRenderer().render(all_rows)
        return HttpResponse(
            json_data, content_type='application/json'
        )

    @action(methods=['post'], detail=True)
    def row(self, request, pk):
        json_data = request.body
        stream = io.BytesIO(json_data)
        python_data = JSONParser().parse(stream)
        new_row = add_row(pk, python_data)
        json_data = JSONRenderer().render(new_row)
        return HttpResponse(
            json_data, content_type='application/json'
        )
