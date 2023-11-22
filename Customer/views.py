from django.shortcuts import render
from multiprocessing import context
from os import stat
from django.db.models.query import Prefetch
from .serializers import *
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from django.utils.timezone import make_aware
from datetime  import date, timedelta, datetime
import datetime
from .models import LastUpdateDate
# Create your views here.

from django.contrib.auth import get_user_model 

User = get_user_model()



def update_date(instance, module):
    current_date = datetime.datetime.now()
    timezone_aware_date = make_aware(current_date)
    customer = User.objects.filter(id=instance.customer.id).first()
    LastUpdate, created = LastUpdateDate.objects.get_or_create(customer=customer)

    instanceDate = instance.date
    if isinstance(instanceDate, str):
        instanceDate = instanceDate.replace('-','')
        instanceDate = datetime.datetime.strptime(instanceDate, '%Y%m%d').date()

    if module == 'diet' and instanceDate >= LastUpdate.diet.date():
        LastUpdate.diet = timezone_aware_date
    elif module == 'activity' and instanceDate >= LastUpdate.activity.date():
        LastUpdate.activity = timezone_aware_date
    elif module == 'medicine' and instanceDate >= LastUpdate.medicine.date():
        LastUpdate.medicine = timezone_aware_date
    elif module == 'symptom' and instanceDate >= LastUpdate.symptom.date():
        LastUpdate.symptom = timezone_aware_date
    
    else:
        # LastUpdate.contraction = timezone_aware_date
        pass
    LastUpdate.save()

@api_view(['GET',])
@permission_classes((IsAuthenticated,))
def medicine_get(request):
    user = request.user
    if not user.role == 'SALES':
        # from calender
        date = request.query_params.get('date', None)
        cid = user.id if user.role == 'CLIENT' else request.query_params.get('customer', None)
        
        if cid is None:
            return Response({"Error" : "Provide id in params as customer:id"}, status=status.HTTP_400_BAD_REQUEST)
        # if date == None:
        #     date = datetime.datetime.now()
        # else:
        #     date = datetime.datetime.strptime(date, '%Y-%m-%d')
        date = date if date is not None else datetime.datetime.now().date()
        data = MedicineTime.objects.all().prefetch_related(
            Prefetch('Medicines',queryset=Medicines.objects.filter(customer=cid, date__lte=date)),
            Prefetch('Medicines__MedicineDetail',queryset=TakenMedicine.objects.filter(date=date))
        )
        serializer = MedicineTimeSerializer(data, many=True)
        return Response(serializer.data)
    else:
        return Response({'error' : 'unauthorized request'}, status=status.HTTP_401_UNAUTHORIZED)
    


@api_view(['POST',])
@permission_classes((IsAuthenticated,))
def medicine_post(request):
    user = request.user
    if user.role == 'CLIENT' or user.role == 'SALES':
        data = request.data.copy()
        if user.role == 'CLIENT':
            data['customer'] = user.id
        else:
            cid = request.data.get('customer', None)
            if cid is not None:
                try:
                    customer = User.objects.get(id=cid)
                    data['customer'] = customer.id
                except User.DoesNotExist:
                    return Response({'error' : 'Client not found'}, status=status.HTTP_404_NOT_FOUND)
            else:
                return Response({'error' : 'provide customer in data'}, status=status.HTTP_400_BAD_REQUEST)

        medTime = request.data.get('medicationTime', None)
        if medTime is not None:
            try:
                med_time = MedicineTime.objects.get(name=medTime)
            except MedicineTime.DoesNotExist:
                return Response({"error" : "Medicine Time not found"}, status=status.HTTP_404_NOT_FOUND)
        else:
            return Response({"error" : "Medicine Time cannot be empty"})

        data['time'] = med_time.id
        serializer = AddMedicineSerializer(data=data)

        if serializer.is_valid(raise_exception=True):
            instance = serializer.save()
            update_date(instance,"medicine")
            return Response({'Success': 'Successfull', 'data': serializer.data})
        else:
            return Response({'Error': serializer.errors})
    else:
        return Response({'error' : 'unauthorized request'}, status=status.HTTP_401_UNAUTHORIZED)
    





@api_view(['POST','PATCH'])
@permission_classes((IsAuthenticated,))
def medicine_update(request):
    user = request.user
    if user.role == 'SALES' or user.role == 'CLIENT':
        date = request.data.get('date', None)
        medicine = request.data.get('medicine', None)
        taken = request.data.get('taken', None)
        if user.role == 'CLIENT':
            customer = request.user
        else:
            customer = request.data.get('customer', None)
            if customer is None:
                return Response({"Error" : "Provide 'customer':id in data"}, status=status.HTTP_400_BAD_REQUEST)
            try:
                customer = User.objects.get(id=customer)
            except User.DoesNotExist:
                return Response({"Error" : "customer not found"}, status=status.HTTP_404_NOT_FOUND)
        try:
            med = Medicines.objects.get(id=medicine)
        except Medicines.DoesNotExist:
            return Response({"Error" : "Medicine not found"}, status=status.HTTP_404_NOT_FOUND)

        if date and taken is not None:
            instance, created = TakenMedicine.objects.get_or_create(medicine=med, date=date, customer=customer,
            defaults={'taken': taken})
            if not created: #then its False, so delete the entry
                instance.taken = taken
                instance.save()
            update_date(instance, "medicine")
            return Response({'succes':'Medicine Updated successfuly'}, status=status.HTTP_202_ACCEPTED)

        else:
            return Response({"Error" : "Date/taken data not provided"}, status=status.HTTP_400_BAD_REQUEST)
    else:
        return Response({'error' : 'unauthorized request'}, status=status.HTTP_401_UNAUTHORIZED)
    

@api_view(['GET',])
@permission_classes((IsAuthenticated,))
def all_medicines(request):
    user = request.user
    if not user.role == 'SALES':
        cid = user.id if user.role == 'CLIENT' else request.query_params.get('customer', None)
        # cid = 5
        if cid is not None:
            # ? new response
            data = TakenMedicine.objects.filter(customer=cid, taken=True).prefetch_related('medicine', 'medicine__time').order_by('-date')
            serializer = TakenMedicineSerializer(data, many=True)
            
            return Response(serializer.data)
        else:
            return Response({"Error" : "Customer is not provided"}, status=status.HTTP_400_BAD_REQUEST)
    else:
        return Response({'error' : 'unauthorized request'}, status=status.HTTP_401_UNAUTHORIZED)