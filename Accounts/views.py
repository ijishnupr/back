from django.shortcuts import render
from rest_framework.views import APIView
from .serializers import *
from .models import *
from django.http import JsonResponse
from rest_framework import status


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