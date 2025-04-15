from rest_framework import serializers


class OutputDataBaseSerializer(serializers.Serializer):
    pass


class OutputDataReadSerializer(serializers.Serializer):
    id = serializers.UUIDField()
    full_name = serializers.CharField()
    timestamp = serializers.DateTimeField()
    is_satisfied = serializers.BooleanField()


class DetailedOutputDataReadSerializer(OutputDataReadSerializer):
    age = serializers.IntegerField()

