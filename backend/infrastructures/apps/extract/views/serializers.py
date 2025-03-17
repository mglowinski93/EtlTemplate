from rest_framework import serializers

class ExtractDataBaseSerializer(serializers.Serializer):
    pass

class ExtractDataSerializer(serializers.Serializer):
    file_path = serializers.CharField(min_length=1)
