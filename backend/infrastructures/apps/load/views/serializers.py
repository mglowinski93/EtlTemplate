from rest_framework import serializers
from dataclasses import asdict
from modules.data.domain import value_objects as data_value_objects
from typing import List


class ExtractDataSerializer(serializers.Serializer):
    file_path = serializers.CharField(min_length=1)


class OutputDataSerializer(serializers.Serializer):
    full_name = serializers.CharField()
    age = serializers.IntegerField()
    is_satisfied = serializers.BooleanField()

# class OutputDataListSerializer(serializers.ListSerializer):
#     child = OutputDataSerializer()

#     def to_representation(self, data: List[data_value_objects.OutputData]):
#         return [asdict(item) for item in data]
    
#     def create(self, validated_data):
#         return [data_value_objects.OutputData(**item) for item in validated_data]
