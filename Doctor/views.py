from django.shortcuts import render
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from Accounts.models import DoctorDetails, CustomerDetails
from .serializers import CustomerDetailsSerializer
from Accounts.serializers import *
@api_view(['GET'])
@permission_classes([])  # You might need to define your permission classes
def customers_under_doctor(request):
    # Get the currently logged-in user, assuming you're using Django's authentication
    user = request.user

    # Find the DoctorDetails record associated with the logged-in user
    try:
        doctor = DoctorDetails.objects.get(user=user)
    except DoctorDetails.DoesNotExist:
        return Response(
            {"error": "You are not associated with any doctor account."},
            status=status.HTTP_404_NOT_FOUND
        )

    # Retrieve all customers with doctor_referal set to the selected doctor
    customers = CustomerDetails.objects.filter(doctor_referal=doctor)

    # Serialize the customer data
    serializer = CustomerDetailsSerializer(customers, many=True)

    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_doctors(request):
    doctors = DoctorDetails.objects.filter(
        user__is_active=True,
        user__role=User.ROLES[1][0]  # Assuming 'DOCTOR' is the second role in the choices tuple
    ).prefetch_related('user')

    serializer = DoctorDetailSerializer(doctors, many=True, context={'request': request})

    return Response({
        'status': True,
        'data': serializer.data,
        'message': 'doctors fetched'
    })