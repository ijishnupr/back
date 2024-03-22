from django.contrib import admin
from rest_framework.authtoken.admin import TokenAdmin as BaseTokenAdmin
from rest_framework.authtoken.models import Token
from .models import *
# Register your models here.
admin.site.register(User)
admin.site.register(CustomerDetails)
admin.site.register(SalesTeamDetails)
admin.site.register(ConsultantInfo)
admin.site.register(DoctorDetails)

class CustomTokenAdmin(BaseTokenAdmin):
    search_fields = ('key', 'user__username')  # Adjust as needed

# Register TokenAdmin with your custom subclass
admin.site.register(Token, CustomTokenAdmin)
