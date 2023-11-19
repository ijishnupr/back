from rest_framework import serializers
from Accounts.models import CustomerDetails
from django.contrib.auth import get_user_model

User = get_user_model()

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'email', 'firstname', 'lastname']  # Include any other user fields me want

class CustomerDetailsSerializer(serializers.ModelSerializer):
    referalId = serializers.SerializerMethodField()
    user = UserSerializer()
    class Meta:
        model = CustomerDetails
        fields = ['user', 'address', 'date_of_birth_parent', 'babydob', 'profile_img', 'babyGender', 'referalId']


    def get_referalId(self, obj):
        # Retrieve the referalId from the associated DoctorDetails
        return obj.doctor_referal.referalId if obj.doctor_referal else None