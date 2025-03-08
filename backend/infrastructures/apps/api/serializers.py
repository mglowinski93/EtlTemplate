from rest_framework import serializers


class ExtractDataSerializer(serializers.Serializer):
    file_path = serializers.CharField(min_length=1)

class InputDataSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=100)
    surname = serializers.CharField(max_length=100)
    age = serializers.IntegerField(min_value=0)  # Ensure age is >= 0
    is_satisfied = serializers.BooleanField()
