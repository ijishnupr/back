from django.urls import path
from .views import *

urlpatterns = [
  
   path('full-appointment/', full_apointments),
   path('completed-appointment/', completed),
    path('upcoming-appointments/', upcoming),
    path('get-doctor-appointments/<id>/' , get_doctor_appointments),
]

