from django.urls import path
from .views import *

urlpatterns = [
  path('customer-booking/', customer_booking),
   path('full-appointment/', full_apointments),
   path('completed-appointment/', completed),
    path('upcoming-appointments/', upcoming),
    path('get-doctor-appointments/<id>/' , get_doctor_appointments),
     path('approve-appointment/', approve),
      # path('reject-appointment/', reject),
]

