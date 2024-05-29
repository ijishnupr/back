
from multiprocessing import context
from Accounts.models import CustomerDetails, DoctorDetails
# from django.shortcuts import render

# from Doctor.models import AppointmentSummary
from .serializers import *
from django.http import JsonResponse
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework import status
# from rest_framework.renderers import JSONRenderer
from rest_framework.permissions import IsAuthenticated, AllowAny
# from rest_framework_api_key.permissions import HasAPIKey
from django.db.models import Q
from .models import Appointments
from django.conf import settings
from datetime import date, datetime, timedelta
# from django.utils import timezone
from twilio.rest import Client
import jwt
import requests
import json
from time import time 
from django.utils.timezone import make_aware
from django.db.models import Q,Case,When, Value, BooleanField

@api_view(['GET',])
@permission_classes((IsAuthenticated,))
def full_apointments(request):
    user = request.user
    if user.role == 2:
        doctor = user.id
        try:
            doctor = DoctorDetails.objects.get(user=doctor)
        except DoctorDetails.DoesNotExist:
            return JsonResponse({"error" : "doctor not found"}, status=status.HTTP_404_NOT_FOUND)
        
        current_timestamp = make_aware(datetime.now())
        dateTimeCompleted = datetime.now() - timedelta(minutes=60)

        approved = Appointments.objects.filter(doctor=doctor.id ,is_paid = True,approved=True,schedule__gte=current_timestamp - timedelta(minutes=15)).prefetch_related('customer','customer__user').order_by('-schedule').annotate(
            meeting_open=Case(
                    When(schedule__range=[current_timestamp - timedelta(minutes=15), current_timestamp], then=Value(True)),default=Value(False), output_field=BooleanField()
                )
        )
        
        rejected = Appointments.objects.filter(doctor=doctor.id , is_paid = True,rejected=True).prefetch_related('customer','customer__user').order_by('-schedule')
        completed = Appointments.objects.filter(doctor=doctor.id, is_paid = True,approved=True,schedule__lte=make_aware(dateTimeCompleted)).prefetch_related('customer','customer__user').order_by('-schedule')

        ApprovedSerializer = BookingSerializer(approved, many=True, context={'request': request})
        RejectedSerializer = BookingSerializer(rejected, many=True, context={'request': request})
        CompletedSerializer = BookingSerializer(completed, many=True, context={'request': request})

        return JsonResponse({
            # "Reschuduled" : RescheduleSerializer.data,
            "Approved" : ApprovedSerializer.data,
            "Rejected" : RejectedSerializer.data,
            "Completed" : CompletedSerializer.data
        })
    else:
        return JsonResponse({'error' : 'unauthorized request'}, status=status.HTTP_401_UNAUTHORIZED)
    
@api_view(['GET',])
@permission_classes((IsAuthenticated,))
def completed(request):
    user = request.user
    if user:
        dateTimeCompleted = datetime.now() - timedelta(minutes=60)
        try:
            client = user.customer_details.get(user=user.id)
        except:
            return JsonResponse({"error" : "client not found"}, status=status.HTTP_404_NOT_FOUND)
        # dateTime = datetime.now() - timedelta(minutes=30)
        
        completedAppointments = Appointments.objects.filter(is_paid = True ,customer=client.id,approved=True, schedule__lte=make_aware(dateTimeCompleted)).prefetch_related('doctor', 'doctor__user').order_by('-schedule')
        serializer = CompletedSerializer(completedAppointments, many=True, context={'request' : request})
        return JsonResponse(serializer.data, safe=False)
    else:
        return JsonResponse({'error' : 'unauthorized request'}, status=status.HTTP_401_UNAUTHORIZED)


@api_view(['GET',])
@permission_classes((IsAuthenticated,))
def upcoming(request):
    user = request.user
    if user:
        try:
            client = user.customer_details.first()
        except:
            return JsonResponse({"error" : "client not found"}, status=status.HTTP_404_NOT_FOUND)
        timestamp = datetime.now() - timedelta(minutes=15)
        upcoming_appointments = Appointments.objects.filter(is_paid = True ,customer=client.id, approved=True, schedule__gte=make_aware(timestamp)).prefetch_related('doctor', 'doctor__user')
        serializer = UpcomingAppointmentSerializer(upcoming_appointments, many=True, context={'request':request})
    else:
        return Response({'error' : "unauthorized request"}, status=status.HTTP_401_UNAUTHORIZED)
    return JsonResponse(serializer.data, safe=False)


@api_view(['GET'])
@permission_classes((IsAuthenticated,))
def get_doctor_appointments(request ,id):
    try:
        doctor = DoctorDetails.objects.get(user__id = id)
        queryset = Appointments.objects.filter(doctor = doctor,completed = True)

        serializer = NewDoctorSerializer(doctor,context={
            'request' : request,
            'sort_by' : request.GET.get('sort_by' ,'asc'),
            'search' : request.GET.get('search' , None)
            
            })
        return Response({
            'status' : True,
            'data' : serializer.data,
            'message' : 'doctors fetched'
        })
    except Exception as e:
        
        return Response({
            'status' : False,
            'data' : {},
            'message' : 'invalid doctor id'
        })


@api_view(['POST',])
@permission_classes((IsAuthenticated,))
def customer_booking(request):
    user = request.user
    if user.role == 3:
        doctor = request.data.get('doctor', None)
        date = request.data.get('date', None)
        time = request.data.get('time', None)
        customer = request.user.id

        doctor_info = {}
        doctor_price = None
        if doctor is not None:
            try:
                doctor = DoctorDetails.objects.select_related('user').get(user=doctor)
                doctor_price = doctor.price
                doctor_info = {
                    "doctor_name" : doctor.user.firstname,
                    "doctor_speciality" : doctor.speciality,
                    "doctor_age" : doctor.age,
                    "doctor_price" : doctor.price,
                    "doctor_qualification" : doctor.qualification,
                    "doctor_interests" : doctor.interests,
                    "doctor_experience" : doctor.experience,
                    "doctor_languages" : doctor.languages,
                    
                    "doctor_gender" : doctor.gender,
                }
            except DoctorDetails.DoesNotExist:
                return JsonResponse({"Error" : "doctor does not exist"}, status=status.HTTP_404_NOT_FOUND)
            try:
                customer = CustomerDetails.objects.get(user=request.user.id)
            except User.DoesNotExist:
                return JsonResponse({"Error" : "Customer does not exist"}, status=status.HTTP_404_NOT_FOUND)
        else:
            return JsonResponse({"Error" : "Customer and doctor are required to make an appointment."})

        data = request.data.copy()
        data['customer'] = customer.id
        data['doctor'] = doctor.id

        if doctor_price is not None and doctor_price <= 0:
            data['is_paid'] = True

        try:
            schedule = datetime.combine(datetime.fromisoformat(date), datetime.strptime(time.replace(" ", ""), '%H:%M').time()) # without pm
        except:
            schedule = datetime.combine(datetime.fromisoformat(date), datetime.strptime(time.replace(" ", ""), '%H:%M%p').time()) # with am and pm
        data['schedule'] = schedule

        serializer = BookingSerializer(data=data, context={'request': request})

        if serializer.is_valid(raise_exception=True):
            appointment = serializer.save()
            data = serializer.data
            data['doctor_info'] = doctor_info
            return JsonResponse(data)
        else:
            return JsonResponse(serializer.errors)
    else:
        return JsonResponse({'error' : 'unauthorized request'}, status=status.HTTP_401_UNAUTHORIZED)
# getting approved


@api_view(['POST',])
@permission_classes((IsAuthenticated,))
def reject(request):
    user = request.user
    if user.role == 2 or user.role == 3:
        appointmentID = request.data.get('appointmentID', None)
        if appointmentID is not None:
            try:
                appointment = Appointments.objects.get(id=appointmentID)
            except Appointments.DoesNotExist:
                return JsonResponse({"error" : "Appointment not found"}, status=status.HTTP_404_NOT_FOUND)
            
            # payments = AppointmentPayments.objects.filter(appointment=appointmentID,captured=True)
            # if payments:
            #     payment = payments.first()
            #     client.payments.refund(payment.payment_id,{
            #         "amount": payment.amount,
            #         "speed": "optimum"
            #     })

            appointment.rejected = True
            appointment.approved = False
            appointment.rescheduled_by_doctor = False
            appointment.rescheduled_by_client = False
            appointment.save()
            
            
            # serializer = BookingSerializer(appointment)

            return JsonResponse({"Success" : "appointment rejected"})
        else:
            return JsonResponse({"Error" : "appointmentID is required"}, status=status.HTTP_400_BAD_REQUEST)
    else:
        return JsonResponse({'error' : 'unauthorized request'}, status=status.HTTP_401_UNAUTHORIZED)


@api_view(['POST',])
@permission_classes((IsAuthenticated,))
def approve(request):
    user = request.user
    if user.role == 2:
        appointmentID = request.data.get('appointmentID', None)
        if appointmentID is not None:
            try:
                appointment = Appointments.objects.select_related('customer', 'customer__user').get(id=appointmentID)
            except Appointments.DoesNotExist:
                return JsonResponse({"error" : "Appointment not found"}, status=status.HTTP_404_NOT_FOUND)
            meeting_url = "createMeeting()"
            appointment.approved = True
            appointment.rejected = False
            appointment.rescheduled = False
            appointment.meeting_url = meeting_url
            appointment.save()

           
            return JsonResponse({"Success" : "Appointment approved."})
        else:
            return JsonResponse({"Error" : "appointmentID is required"}, status=status.HTTP_400_BAD_REQUEST)
    else:
        return JsonResponse({'error' : 'unauthorized request'}, status=status.HTTP_401_UNAUTHORIZED)
