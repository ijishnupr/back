from django.shortcuts import render
from rest_framework.views import APIView
from .serializers import *
from .models import *
from django.http import JsonResponse
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.permissions import IsAuthenticated, AllowAny, IsAdminUser, BasePermission
from rest_framework import generics
from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from django.http import Http404
from rest_framework.decorators import api_view, permission_classes
from django.contrib.auth import authenticate,login
from django.db.models import Q
from django.db.models import Prefetch
from Consultant.serializers import *
from django.contrib.auth import get_user_model, password_validation as password_validators
from django.core import exceptions
# Create your views here.
class UserRegistrationView(APIView):
    def post(self, request):
        data = request.data
        serializer = UserPostNatalSerializer(data=data)

        if serializer.is_valid():
            # Create the user instance
            user = User.objects.create_user(
                email=serializer.validated_data['email'],
                firstname=serializer.validated_data['firstname'],
                lastname=serializer.validated_data['lastname'],
                mobile=serializer.validated_data['mobile'],
                fcm_token=serializer.validated_data['fcm_token'],
                password=serializer.validated_data['password']  # Set the password
            )

            # Create CustomerDetails for the user
            customer_details_data = {
                "user": user.pk,  # Pass the user's primary key
                "address": "",  # Add any other fields as needed
                "date_of_birth_parent": None,
                "babydob": None,
                "babyGender": None
            }
            customer_details_serializer = CustomerDetailsSerializer(data=customer_details_data)

            if customer_details_serializer.is_valid():
                customer_details_serializer.save()
            else:
                # Handle errors with CustomerDetails creation
                user.delete()  # Delete the user if CustomerDetails creation fails
                return Response(
                    customer_details_serializer.errors,
                    status=status.HTTP_400_BAD_REQUEST
                )

            return Response({'message': 'User registered successfully'}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
@api_view(['POST'])
def doctor_registration(request):
    serializer = DoctorRegistrationSerializer(data=request.data)

    if serializer.is_valid():
        user_data = {
            'email': serializer.validated_data['email'],
            'password': serializer.validated_data['password'],
            'firstname': serializer.validated_data['firstname'],
            'lastname': serializer.validated_data['lastname'],
        }
        
        # Create a new user
        user_data['role'] = 2
        user = User.objects.create_user(**user_data)

        # Create the associated doctor details
        doctor_details_data = {k: v for k, v in serializer.validated_data.items() if k not in user_data}
        DoctorDetails.objects.create(user=user, **doctor_details_data)

        return Response({'success': 'Successfully registered'}, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

from django.contrib.auth import login as django_login
from django.http import JsonResponse
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from .models import User  # Import your custom token model
from .serializers import UserPostNatalSerializer

# @api_view(['POST'])
# @permission_classes([AllowAny])
# def login_view(request):
#     data = request.data
#     email = data.get('email')
#     password = data.get('password')

#     try:
#         user_postnatal = User.objects.get(email=email)
#     except User.DoesNotExist:
#         user_postnatal = None

#     if user_postnatal is not None and user_postnatal.check_password(password):
#         if not user_postnatal.is_active:
#             return JsonResponse(
#                 {
#                     "error": "Please call your salesperson to activate this account."
#                 },
#                 status=status.HTTP_401_UNAUTHORIZED
#             )
#         else:
#             # Log the user in with the specified backend
#             user_postnatal.backend = 'django.contrib.auth.backends.ModelBackend'  # Set the backend
#             django_login(request, user_postnatal)  # Log in the user

#             # Check if the user already has a token
#             token, created = Token.objects.get_or_create(user=user_postnatal)

#             return JsonResponse(
#                 {
#                     "message": "User is logged in successfully.",
#                     "token": token.key  # Include the token in the response
#                 },
#                 status=status.HTTP_200_OK
#             )
#     else:
#         return JsonResponse(
#             {
#                 "error": "Login failed"
#             },
#             status=status.HTTP_401_UNAUTHORIZED
#         )


@api_view(['POST'])
@permission_classes([AllowAny])
def login_view(request):
    data = request.data
    email = data.get('email')
    password = data.get('password')

    try:
        user_postnatal = User.objects.get(email=email)
    except User.DoesNotExist:
        user_postnatal = None

    if user_postnatal is not None and user_postnatal.check_password(password):
        if not user_postnatal.is_active:
            return JsonResponse(
                {
                    "error": "Please call your salesperson to activate this account."
                },
                status=status.HTTP_401_UNAUTHORIZED
            )
        else:
            # Log the user in with the specified backend
            user_postnatal.backend = 'django.contrib.auth.backends.ModelBackend'  # Set the backend
            django_login(request, user_postnatal)  # Log in the user

            # Check if the user already has a token
            token, created = Token.objects.get_or_create(user=user_postnatal)

            return JsonResponse(
                {
                    "message": user_postnatal.role,
                    "token": token.key  # Include the token in the response
                },
                status=status.HTTP_200_OK
            )
    else:
        return JsonResponse(
            {
                "error": "Login failed"
            },
            status=status.HTTP_401_UNAUTHORIZED
        )
    

@api_view(['POST'])
@permission_classes((IsAuthenticated,))
# @authentication_classes([TokenAuthentication])
def logout_view(request):
    customer = request.user.id
    if customer is not None:
        try:
            token = Token.objects.get(user=customer)
            token.delete()
            return JsonResponse({'message': 'User logged out successfully'})
        except Token.DoesNotExist:
            return JsonResponse({'message': 'User already logged out'}, status=status.HTTP_400_BAD_REQUEST)
    else:
        return JsonResponse({"Error": "User customer not provided"}, status=status.HTTP_400_BAD_REQUEST)
    

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_customer_details(request):
    user = request.user  # Retrieve the user associated with the token

    try:
        customer_details = CustomerDetails.objects.get(user=user)
        serializer = CustomerDetailsSerializer(customer_details)
        return Response(serializer.data, status=200)
    except CustomerDetails.DoesNotExist:
        return Response({"error": "Customer details not found for this user."}, status=404)


from django.views.decorators.csrf import csrf_exempt

@api_view(['POST'])  # Change to POST
@permission_classes([IsAuthenticated])
@csrf_exempt
def update_customer_details(request):
    user = request.user  # Retrieve the user associated with the token
    print(f"User: {user}")  # Print user for debugging
    print(f"Request Data: {request.data}")

    try:
        customer_details = CustomerDetails.objects.get(user=user)
    except CustomerDetails.DoesNotExist:
        return Response({"error": "Customer details not found for this user."}, status=404)

    serializer = CustomerDetailsSerializer(customer_details, data=request.data, partial=True)

    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=200)
    else:
        return Response(serializer.errors, status=400)
    

@api_view(['PATCH'])
@permission_classes([IsAuthenticated])
def admin_update_customer_details(request):
    # Get the user_id from the query parameters
    user_id = request.GET.get('user_id')

    # Check if user_id is a valid integer
    try:
        user_id = int(user_id)
    except (TypeError, ValueError):
        return JsonResponse({'error': 'Invalid user_id'}, status=400)

    # Check if the user exists
    try:
        user = User.objects.get(pk=user_id)
    except User.DoesNotExist:
        return JsonResponse({'error': 'User not found'}, status=404)

    # Check if the user has associated customer details
    try:
        customer_details = CustomerDetails.objects.get(user=user)
    except CustomerDetails.DoesNotExist:
        return JsonResponse({'error': 'Customer details not found for this user.'}, status=404)

    # Update customer details based on the request data
    if request.method == 'PATCH':
        serializer = CustomerDetailsSerializer(customer_details, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, status=200)
        else:
            return JsonResponse(serializer.errors, status=400)
    else:
        return JsonResponse({'error': 'Invalid request method. Use PATCH to update customer details.'}, status=400)
    


@api_view(['POST'])
@permission_classes([AllowAny])
def sales_team_registration(request):
    serializer = SalesTeamRegistrationSerializer(data=request.data)
    if serializer.is_valid():
        user = serializer.save()
        return Response({"message": "SALES team registered successfully."}, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



@api_view(['POST'])
@permission_classes([AllowAny])
def consultant_registration(request):
    serializer = ConsultantTeamRegistrationSerializer(data=request.data)
    if serializer.is_valid():
        user = serializer.save()
        return Response({"message": "Consultant registered successfully."}, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# admin section
from django.db.models import Count
from payment.serializers import *

@api_view(['POST'])
@permission_classes([AllowAny])
def signup_admin(request):
    email=request.data.get('email')
    password=request.data.get('password')
    fname=request.data.get('fname')
    lname=request.data.get('lname')
    if email and password is not None:
        user=User.objects.create_user(email=email,password=password,role=1,firstname=fname,lastname=lname)
        return Response({'message':'created user'})
    else:
        return Response({'error':'enter email and password'})



@api_view(['POST'])
@permission_classes([AllowAny])
def login_admin(request):
    email=request.data.get('email')
    password=request.data.get('password')
    user=authenticate(request,email=email,password=password)
    if user:
        login(request,user)
        token,created=Token.objects.get_or_create(user=user)

        return Response({'token':token.key})
    return Response('user not found',status=401)


@api_view(['GET'])
@permission_classes((IsAuthenticated,))
def admin_dashboard(request):
    user = request.user
    if user:
        counts = User.objects.aggregate(
            totalConsultant=Count('id', filter=Q(role=User.CONSULTANT,is_active=True, consultantDetails__isnull = False)),
            totalSalesTeam=Count('id', filter=Q(role=User.SALES,is_active=True)),
            activeClients=Count('id', filter=Q(role=User.CLIENT,is_active=True)),
            disabledDoctors=Count('id', filter=Q(role=User.DOCTOR,is_active=False)),
            totalDoctors=Count('id', filter=Q(role=User.DOCTOR,is_active=True)),
            totalClients=Count('id', filter=Q(role=User.CLIENT,is_active=True)))

        print(counts)

        CountSerializer = adminDashboardCountsSerializer(counts)
    
        clientDetails = CustomerDetails.objects.all()
        clientDetails = totalClientSerializer.pre_loader(clientDetails)
        serializer = totalClientSerializer(clientDetails, many=True, context={'request' : request})

        memberships = MemberShip.objects.all()
        membershipSerialized = Membership2Serializer(memberships, many=True)   

        context = {
            "MemberShipPlans" : membershipSerialized.data,
            "counts" : CountSerializer.data,
            # "totalDoctors" : totalDoctors.count(),
            # "totalClients" : totalClients.count(),
            # "totalHospitals" : totalHospitals,
            # "totalConsultant" : totalConsultant,
            # "totalSalesTeam" : totalSalesTeam,
            # "activeClients" : activeClients,
            # "disabledDoctors" : disabledDoctors,
            "clientDetails" : serializer.data
        }
        return JsonResponse(context)
    else:
        return JsonResponse({'error' : 'unauthorized request'}, status=status.HTTP_401_UNAUTHORIZED)
@api_view(['GET',])
@permission_classes((IsAuthenticated,))
def all_doctors(request):
    user = request.user
    if user:
        doctors = DoctorDetails.objects.filter(Q(user__is_active__in=[True])).prefetch_related('user')
        serializer = DoctorDetailSerializer(doctors, many=True,context={'request' : request})
        print('done')
        return JsonResponse(serializer.data, safe=False)
    else:
        return JsonResponse({'error' : 'unauthorized request'}, status=status.HTTP_401_UNAUTHORIZED)


@api_view(['GET',])
@permission_classes((IsAuthenticated,))
def all_sales_team(request):
    try:

        user = request.user
        sales = SalesTeamDetails.objects.filter(user__isnull = False, user__role = 4).prefetch_related('user')
        if user.role == User.ADMIN:
            serializer = SalesTeamSerializer(sales, many=True)
        # elif user.role == User.CLIENT:
        #     serializer = SalesSerializer(sales,many=True, context={'request':request})
        else:
            return JsonResponse({'error' : 'unauthorized request'}, status=status.HTTP_401_UNAUTHORIZED)
        context = {
            'count' : len(serializer.data),
                'details' : serializer.data
            }
        return JsonResponse(context)
    except Exception as e:
        pass

@api_view(['POST'])
@permission_classes((IsAuthenticated,))
def activate_or_deactivate(request):
    user = request.user
    if user.role == User.ADMIN or user.role == User.HOSPITAL_MANAGER:
        userID = request.data.get('id', None)
        if userID is not None:
            try:
                user = User.objects.get(id=userID)
            except User.DoesNotExist:
                return JsonResponse({"Error" : "User not found"}, status=status.HTTP_404_NOT_FOUND)
            Token.objects.filter(user=user).delete()
            user.is_active = not user.is_active
            user.save()
            if user.is_active:
                state = "Activated"
            else:
                state = "Deactivated"
            return JsonResponse({"Success" : "Account " + state})
        else:   
            return JsonResponse({"Error" : "id not provided"}, status=status.HTTP_400_BAD_REQUEST)
    else:
        return JsonResponse({'error' : 'unauthorized request'}, status=status.HTTP_401_UNAUTHORIZED)

@api_view(['GET'])
@permission_classes((IsAuthenticated,))
def all_consultants_list(request):
    user = request.user
    consultants = ConsultantInfo.objects.filter(user__role = 5).prefetch_related('user')
    if user.role == User.ADMIN:
        serializer = ConsultantInfoSerializer(consultants, many=True, context={'request' : request})
    elif user.role == User.CLIENT:
        serializer = ConsultantSerializer(consultants, many=True, context={'request':request})
    else:
        return JsonResponse({'error' : 'unauthorized request'}, status=status.HTTP_401_UNAUTHORIZED)
    return JsonResponse({'data' : serializer.data, 'count' :consultants.count() }, safe=False)


@api_view(['GET'])
@permission_classes((IsAuthenticated,))
def doctor_approval_requests(request):
    user = request.user
    if user.role == User.ADMIN:
        doctors = DoctorDetails.objects.filter(user__is_active=False).prefetch_related('user', 'hospitalManager')
        serializer = DoctorDetailSerializer(doctors, many=True, context={'request' : request})
        return JsonResponse(serializer.data, safe=False)
    else:
        return JsonResponse({'error' : 'unauthorized request'}, status=status.HTTP_401_UNAUTHORIZED)

@api_view(['PATCH'])
@permission_classes((IsAuthenticated,))
def password_change(request):
    user = request.user
    if user.role == User.CLIENT or user.role == User.DOCTOR:
        password = request.data.get('password', None)
        PasswordErrors = dict() 
        if password is not None:
            try:
                password_validators.validate_password(password=password, user=User)
            except exceptions.ValidationError as e:
                PasswordErrors['password'] = list(e.messages)
                return JsonResponse(PasswordErrors, status=status.HTTP_400_BAD_REQUEST)
            user.set_password(password)
            user.save()
            return JsonResponse({'success' : 'password changed successfully'})
    else:
        return JsonResponse({'error', 'unauthorized request'}, status=status.HTTP_401_UNAUTHORIZED)



@api_view(['GET',])
@permission_classes((IsAuthenticated,))
def customer_profile(request):
    user = request.user
    if user:
        if user.role == User.CLIENT:
            cid = user.id
        else:
            cid = request.query_params.get('customer', None)
            
        if cid is not None:
            try:
                customer = User.objects.get(id=cid)
            except User.DoesNotExist:
                return JsonResponse({"error" : "Customer not found"}, status=status.HTTP_404_NOT_FOUND)

            try:
                details = CustomerDetails.objects.get(user=cid)
            except CustomerDetails.DoesNotExist:
                return JsonResponse({"error" : "Customer details not found."}, status=status.HTTP_404_NOT_FOUND)

            customer = RegistrationSerializers(customer,context={'request':request})
            details = CustomerDetailsSerializer(details)

            context = {
                "customer" : customer.data,
                "details" : details.data
            }
            print('this is the value to the frontend',context)
            return JsonResponse(context, status=status.HTTP_200_OK)
        else:
            return JsonResponse({"Error" : "Customer is None"}, status=status.HTTP_400_BAD_REQUEST)
    else:
        return JsonResponse({'error' : 'unauthorized request'}, status=status.HTTP_401_UNAUTHORIZED)


@api_view(['PATCH'])
@permission_classes([IsAuthenticated,])
def admin_update_customer_data(request):
    user_id = request.query_params.get('user_id')
    if not user_id:
        return Response({"error": "user_id parameter is required."}, status=400)

    try:
        customer = CustomerDetails.objects.get(user__id=user_id)
    except CustomerDetails.DoesNotExist:
        return Response({"error": "Customer not found for the specified user_id."}, status=404)

    serializer = CustomerDetailsSerializer(customer, data=request.data, partial=True)
    if serializer.is_valid():
        serializer.save()
        print(serializer.data)
        return Response(serializer.data)
    return Response(serializer.errors, status=400)