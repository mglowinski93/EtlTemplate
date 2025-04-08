from rest_framework import serializers


class OutputDataBaseSerializer(serializers.Serializer):
    pass


class OutputDataReadSerializer(serializers.Serializer):
    id = serializers.UUIDField()
    full_name = serializers.CharField()
    age = serializers.IntegerField()
    is_satisfied = serializers.BooleanField()

class DetailedOutputDataReadSerializer(serializers.Serializer):
    id = serializers.UUIDField()
    full_name = serializers.CharField()
    age = serializers.IntegerField()
    is_satisfied = serializers.BooleanField()
    timestamp = serializers.DateTimeField()
