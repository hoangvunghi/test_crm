from rest_framework import serializers
from base.models import Customer

class CustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = ['id', 'user', 'phone', 'address', 'is_active']
        read_only_fields = ['id', 'user'] 