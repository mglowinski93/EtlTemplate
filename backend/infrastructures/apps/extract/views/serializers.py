from rest_framework import serializers


class ExtractDataSerializer(serializers.Serializer):
    file_path = serializers.CharField(min_length=1)
