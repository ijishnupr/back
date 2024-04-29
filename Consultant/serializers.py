from rest_framework import serializers
from Accounts.models import *
from django.contrib.sites.shortcuts import get_current_site
class ConsultantSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(source="user.id")
    accountStatus = serializers.BooleanField(source='user.is_active', read_only=True)
    name = serializers.CharField(source='user.firstname', read_only=True)
    email = serializers.EmailField(source='user.email', read_only=True)
    profile_pic = serializers.SerializerMethodField()
    class Meta:
        model = ConsultantInfo
        fields = ['id', 'name', 'email', 'location', 'accountStatus','profile_pic']

    def get_profile_pic(self, obj):
        request = self.context.get('request')
        if obj.user.profile_img:
            return "https://" + str(get_current_site(request)) + "/media/" + str(obj.user.profile_img)
        else:
            return "https://" + str(get_current_site(request)) + "/media/ProfilePic/" + str("default.jpg")
