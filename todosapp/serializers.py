from rest_framework import serializers
from .models import Todos




class TodoSerializers(serializers.ModelSerializer):
    class Meta:
        model = Todos
        fields= '__all__'


class FutureSerializer(serializers.Serializer):
    date = serializers.DateField()