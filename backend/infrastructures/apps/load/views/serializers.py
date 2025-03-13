from rest_framework import serializers


class ExtractDataSerializer(serializers.Serializer):
    file_path = serializers.CharField(min_length=1)


class OutputDataSerializer(serializers.Serializer):
    full_name = serializers.CharField()
    age = serializers.IntegerField()
    is_satisfied = serializers.BooleanField()
