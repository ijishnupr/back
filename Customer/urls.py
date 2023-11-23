from django.urls import path
from .views import *

urlpatterns = [


    path('medicine-POST/', medicine_post), #used to add medicine
    path('medicine-GET/', medicine_get),
    path('medicine-update/', medicine_update),
    path('get_breastfeeding_records/', get_breastfeeding_records, name='get_breastfeeding_records'),
    path('create_breastfeeding_records/', create_breastfeeding_records, name='create_breastfeeding_records'),
    path('edit_breastfeeding_records/', edit_breastfeeding_record, name='edit_breastfeeding_records'),
]