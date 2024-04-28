
from rest_framework import serializers
from .models import *
from datetime import timedelta
from datetime import timedelta, datetime
import sys, os
from Accounts.models import CustomerDetails
class ClientDetialSerializer(serializers.ModelSerializer):
    id = serializers.SerializerMethodField()
    firstName = serializers.SerializerMethodField()
    lastName = serializers.SerializerMethodField()
    doctorFirstName = serializers.SerializerMethodField()
    doctorLastName = serializers.SerializerMethodField()
 
    # membership =serializers.SerializerMethodField()
    # location = serializers.SerializerMethodField()

    class Meta:
        model = CustomerDetails
        fields = '__all__'

    def get_id(self, obj):
        return obj.user.id

    def get_firstName(self, obj):
        return obj.user.firstname

    def get_lastName(self, obj):
        return obj.user.lastname


    def get_doctorFirstName(self,obj):
        try:
            return obj.referalId.user.firstname
        except:
            return ""

    def get_doctorLastName(self, obj):
        try:
            return obj.referalId.user.lastname
        except:
            return ""

class CustomerCallReposnseSerializer(serializers.ModelSerializer):
    # reponse = serializers.PrimaryKeyRelatedField(queryset=CallResponses.objects.all())
    callResponse = serializers.CharField(source='response.response', read_only=True)
    class Meta:
        model = CustomerCallReposnses
        fields = '__all__'
        extra_kwargs = {
            'customer' : {'write_only' : True},
            'response' : {'write_only' : True},
            'sales' : {'write_only' : True}
        }

class CustomerCallReposnsesSerializer(serializers.ModelSerializer):
    response = serializers.CharField(source='response.response', read_only=True)  # Use 'response.response' as the source

    class Meta:
        model = CustomerCallReposnses
        fields = ['customer_id', 'response', 'note', 'date']        
