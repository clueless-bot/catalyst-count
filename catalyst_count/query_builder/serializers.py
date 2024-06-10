# serializers.py
from rest_framework import serializers
from upload_data.models import Data


class UniqueValuesSerializer(serializers.Serializer):
    industries = serializers.ListField(child=serializers.CharField())
    years_founded = serializers.ListField(child=serializers.IntegerField())
    cities = serializers.ListField(child=serializers.CharField())
    states = serializers.ListField(child=serializers.CharField())
    countries = serializers.ListField(child=serializers.CharField())
    total_employee_min = serializers.IntegerField()
    total_employee_max = serializers.IntegerField()


class DataSerializer(serializers.ModelSerializer):
    class Meta:
        model = Data
        fields = "__all__"
