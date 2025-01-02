from rest_framework import serializers
from base.models import Employee

class EmployeeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Employee
        fields = ['id', 'user', 'phone', 'address', 'position', 'is_active']
        read_only_fields = ['id', 'user']  