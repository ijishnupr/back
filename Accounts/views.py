from django.shortcuts import render
from rest_framework.views import APIView
from .serializers import *
from .models import *
from django.http import JsonResponse
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.permissions import IsAuthenticated, AllowAny, IsAdminUser, BasePermission


# Create your views here.
class UserRegistrationView(APIView):
    def post(self, request):
        data = request.data
        serializer = UserPostNatalSerializer(data=data)

        if serializer.is_valid():
            # Create the user instance
            user = UserPostNatal.objects.create_user(
                email=serializer.validated_data['email'],
                firstname=serializer.validated_data['firstname'],
                lastname=serializer.validated_data['lastname'],
                mobile=serializer.validated_data['mobile'],
                babydob=serializer.validated_data['babydob'],
                babyGender=serializer.validated_data['babyGender'],
                fcm_token=serializer.validated_data['fcm_token'],
                profile_img=serializer.validated_data['profile_img'],
                password=serializer.validated_data['password']  # Set the password
            )
            user.save()



            return JsonResponse({'message': 'User registered successfully'}, status=status.HTTP_201_CREATED)
        return JsonResponse(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

from django.contrib.auth import login as django_login
from django.http import JsonResponse
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from .models import UserPostNatal  # Import your custom token model
from .serializers import UserPostNatalSerializer

@api_view(['POST'])
@permission_classes((AllowAny,))
def login_view(request):
    data = request.data
    email = data.get('email')
    password = data.get('password')

    try:
        user_postnatal = UserPostNatal.objects.get(email=email)
    except UserPostNatal.DoesNotExist:
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

            # # Get or create a token for the user using the custom token model
            # token, created = Token.objects.get_or_create(user=user_postnatal)

            return JsonResponse(
                {
                    "message": "User is logged in successfully.",
                    # "token": token.key  # Include the token in the response
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
    

