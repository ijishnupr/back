from rest_framework import serializers
from .models import *

class UserPostNatalSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('email', 'firstname', 'lastname', 'mobile', 'fcm_token','password')
        extra_kwargs = {
            'password': {'write_only': True},
        }


class CustomerDetailsSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomerDetails
        fields = '__all__'  # Include all fields from the CustomerDetails model