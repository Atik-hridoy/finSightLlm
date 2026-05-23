from rest_framework import serializers


class AIRequestSerializer(serializers.Serializer):
    month = serializers.CharField(required=False)
