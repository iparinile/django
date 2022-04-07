from rest_framework import serializers

from .models import Todo


class TodoSerializer(serializers.Serializer):
    title = serializers.CharField(max_length=120)
    description = serializers.CharField()
    completed = serializers.BooleanField(default=False)

    def create(self, validated_data):
        return Todo.objects.create(**validated_data)
