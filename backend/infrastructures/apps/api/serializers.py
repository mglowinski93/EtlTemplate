from rest_framework import serializers
from dataclasses import asdict
from modules.data.domain import value_objects as domain_value_objects
from typing import List


class ExtractDataSerializer(serializers.Serializer):
    file_path = serializers.CharField(min_length=1)


#TODO 5: I am almost sure that serializer for DataFrame doesn't work that way. Please consult and verify it.
class InputDataSerializer(serializers.Serializer):
    name = serializers.CharField()
    surname = serializers.CharField()
    age = serializers.IntegerField(min_value=0)  # Ensure age is >= 0
    is_satisfied = serializers.BooleanField()

    def create(self, validated_data):
        return domain_value_objects.InputData(**validated_data)

class OutputDataSerializer(serializers.Serializer):
    full_name = serializers.CharField()
    age = serializers.IntegerField()
    is_satisfied = serializers.BooleanField()

class OutputDataListSerializer(serializers.ListSerializer):
    child = OutputDataSerializer()

    def to_representation(self, data: List[domain_value_objects.OutputData]):
        return [asdict(item) for item in data]
    
    def create(self, validated_data):
        return [domain_value_objects.OutputData(**item) for item in validated_data]
