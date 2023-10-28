from django.contrib import admin
from django.urls import path, include
from .views import *
urlpatterns = [

    path('register/', UserRegistrationView.as_view(), name='user-registration'),
    path('logout/', logout_view),
]



    


