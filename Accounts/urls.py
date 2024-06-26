from django.urls import path
from .views import *
urlpatterns = [

    path('register/', UserRegistrationView.as_view(), name='user-registration'),
    path('login/', login_view),
    path('logout/', logout_view),
    path('get-customer-details/', get_customer_details, name='get-customer-details'),
    path('update-customer-details/', update_customer_details, name='update-customer-details'),
    path('admin-update-customer-details/',admin_update_customer_details, name='admin-update-customer-details'),
    path('doctor_registration/', doctor_registration, name='doctor_registration'),
    path('sales_team_registration/', sales_team_registration, name='sales_team_registration'),
    path('consultant_registration/', consultant_registration, name='consultant_registration'),
    
    
#admin section 
    path('signup_admin/',signup_admin),
    path('login_admin/',login_admin),
    path('admin_dashboard_details/',admin_dashboard),
    path('all-doctors-list/', all_doctors),
    path('all-salesTeam-list/', all_sales_team ),
     # Activate or deactivate
    path('activateOrDeactivate/', activate_or_deactivate),
    path('all-consultants-list/', all_consultants_list),
    path('doctor-approval-requests/', doctor_approval_requests),
    path('password-change/', password_change),
    path('customer-profile/', customer_profile),
    path('admin-update-customer-data/', admin_update_customer_data),
    path('video/', VideoLinkView.as_view(), ),
    path('banner/' , BannerView.as_view()),
    path('all-clients-list/', all_clients_list),
    path('add_plans/',add_plan),
    path('get_plans/',get_plan),
    path('patch_plan/',patch_plan),
]

   

    


