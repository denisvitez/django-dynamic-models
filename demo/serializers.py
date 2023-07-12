from django.contrib.auth.models import User
from rest_framework import serializers

from demo.models import DynamicTableColumn


class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ['url', 'username', 'email', 'groups']


class DynamicTableColumnSerializer(serializers.Serializer):
    name = serializers.CharField()
    type = serializers.ChoiceField(DynamicTableColumn.SUPPORTED_TYPES)


class DynamicTableSerializer(serializers.Serializer):
    name = serializers.CharField()
    columns = DynamicTableColumnSerializer(many=True)


class DynamicTableBasicSerializer(serializers.Serializer):
    pk = serializers.IntegerField()
    name = serializers.CharField()
