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


from rest_framework.validators import UniqueValidator

class DoctorRegistrationSerializer(serializers.Serializer):
    # User registration fields
    email = serializers.EmailField(required=True)
    password = serializers.CharField(write_only=True, required=True, style={'input_type': 'password'})
    firstname = serializers.CharField(max_length=100, required=True)
    lastname = serializers.CharField(max_length=100, required=False, allow_blank=True)
    
    # Doctor-specific fields
    speciality = serializers.CharField(max_length=200, required=True)
    qualification = serializers.CharField(max_length=200, required=True)
    medicalCouncil = serializers.CharField(max_length=20, required=True)
    councilRegNo = serializers.CharField(max_length=200, required=True)
    hospitals = serializers.CharField(max_length=300, required=True)
    interests = serializers.CharField(max_length=200, required=True)
    placeOfWork = serializers.CharField(max_length=200, required=True)
    onlineConsultation = serializers.CharField(max_length=100, required=True)
    experience = serializers.IntegerField(required=True)
    age = serializers.IntegerField(required=True)
    languages = serializers.CharField(max_length=500, required=True)
    location = serializers.CharField(max_length=200, required=False, allow_blank=True)
    referalId = serializers.CharField(max_length=100, required=False, allow_blank=True)
    price = serializers.IntegerField(required=True)
    gender = serializers.ChoiceField(choices=DoctorDetails.GENDER_CHOICES, required=False, allow_blank=True)