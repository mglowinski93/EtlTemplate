from rest_framework import serializers


class OutputDataBaseSerializer(serializers.Serializer):
    # TODO discuss what to put here
    pass


class OutputDataReadSerializer(serializers.Serializer):
    full_name = serializers.CharField()
    age = serializers.IntegerField()
    is_satisfied = serializers.BooleanField()
