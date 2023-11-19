from django.urls import path
from .views import *

urlpatterns = [
    path('customers_under_doctor/',customers_under_doctor, name='customers_under_doctor'),
    path('get-doctors/' , get_doctors),
]