from django.contrib import admin
from django.urls import path, include
from .views import *
urlpatterns = [

    path('register/', UserRegistrationView.as_view(), name='user-registration'),
    path('login/', login_view),
    path('logout/', logout_view),
    path('get-customer-details/', get_customer_details, name='get-customer-details'),
    path('update-customer-details/', update_customer_details, name='update-customer-details'),
]



    


