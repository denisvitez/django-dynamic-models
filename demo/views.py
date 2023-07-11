from django.shortcuts import render
from django.contrib.auth.models import User
from rest_framework import viewsets
from rest_framework import permissions
from rest_framework.decorators import api_view
from rest_framework.response import Response

from demo.serializers import UserSerializer
from .db_service import create_test_model, delete_test_model
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
        return Response('Hello World')


class TableViewSet(viewsets.ViewSet):
    def list(self, response):
        return Response('XXX')

    def create(self, request):
        create_test_model()
        return Response("OK")

    def destroy(self, request, pk):
        delete_test_model()
        return Response("OK")
