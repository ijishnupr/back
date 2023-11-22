from Accounts.models import *
from rest_framework import serializers
from .models import *
from django.contrib.auth import get_user_model
from django.contrib.sites.shortcuts import get_current_site

User = get_user_model()




class AddMedicineSerializer(serializers.ModelSerializer):
    class Meta:
        model = Medicines
        fields = '__all__'

class TakenMedicineSerializer(serializers.ModelSerializer):
    medicine = serializers.CharField(source='medicine.name') 
    medicationTime = serializers.CharField(source='medicine.time.name') 
    class Meta:
        # list_serializer_class = MedicineFilter
        model = TakenMedicine
        fields = '__all__'
        extra_kwargs = {
            'customer' : {'write_only' : True},
        }
    def to_representation(self, instance):
        representation = super(TakenMedicineSerializer, self).to_representation(instance)
        representation['date'] = instance.date.strftime("%d-%m-%Y")
        return representation
    
class MedicineSerializer(serializers.ModelSerializer):
    taken = serializers.SerializerMethodField()
    MedicationTime = serializers.CharField(source="time.name")
    class Meta:
        model = Medicines
        fields = ['id', 'name', 'taken', 'MedicationTime']
        extra_kwargs = {
            'customer' : {'write_only' : True},
            'time' : {'write_only' : True},
            'taken' : {'read_only' : True},
            'MedicationTime' : {'read_only' : True}
        }
        
    def get_taken(self,obj):
        response = obj.MedicineDetail.first()
        # print(len(connection.queries))
        try:
            return response.taken 
        except:
            return False
        
class MedicineTimeSerializer(serializers.ModelSerializer):
    Medicines = MedicineSerializer(many=True)
    MedicationTime = serializers.CharField(source="name")
    class Meta:
        # print(len(connection.queries))
        model = MedicineTime
        fields = ['MedicationTime', 'Medicines']
    