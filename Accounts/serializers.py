from rest_framework import serializers
from .models import UserPostNatal

class UserPostNatalSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserPostNatal
        fields = ('email', 'firstname', 'lastname', 'mobile', 'babydob', 'babyGender', 'fcm_token', 'profile_img', 'password')
        extra_kwargs = {
            'password': {'write_only': True},
        }