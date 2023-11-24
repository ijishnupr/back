from django.urls import path
from .views import *

urlpatterns = [


    path('medicine-POST/', medicine_post), #used to add medicine
    path('medicine-GET/', medicine_get),
    path('medicine-update/', medicine_update),
    path('get_breastfeeding_records/', get_breastfeeding_records, name='get_breastfeeding_records'),
    path('submit_breastfeeding_records/', submit_breastfeeding_record, name='submit_breastfeeding_record'),
]