from django.urls import path
from .views import *

urlpatterns = [
    path('sales-dashboard-details/', sales_dashboard_details),
    # call response

    path('call-response/', add_call_response),
    path('get-call-response/', get_call_response),
    path('get-all-call-responses/', get_all_call_responses),
    # clients of a sales team

    path('client-this-month/', clients_this_month),
    path('no-update-clients/', no_update_clients),
    
    path('all-clients/', all_clients),
    path('sales-team-called/',sales_team_called_list,)
]
