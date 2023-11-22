from django.urls import path
from .views import *

urlpatterns = [


    path('medicine-POST/', medicine_post), #used to add medicine
    path('medicine-GET/', medicine_get),
    path('medicine-update/', medicine_update)
]