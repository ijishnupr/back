from django.db import models
from Accounts.models import *
# Create your models here.
class PatientDetailsApporval(models.Model):
    doctor = models.ForeignKey(DoctorDetails, on_delete=models.CASCADE)
    customer = models.ForeignKey(CustomerDetails, on_delete=models.CASCADE)
    is_approved = models.BooleanField(default=False)
    date = models.DateTimeField(auto_now_add=True,null=True)
    
    class Meta:
        unique_together = ['doctor', 'customer']
        ordering = ['-date']


    def __str__(self) :
        return self.doctor.user.firstname + " " + self.customer.user.firstname
class CallResponses(models.Model):
    response = models.CharField(max_length=200)

    def __str__(self):
        return self.response
    class Meta:
        verbose_name = "CallResponses (Manual)"

# to keep the response by customers 
class CustomerCallReposnses(models.Model):
    customer = models.ForeignKey(User, on_delete=models.CASCADE)
    response = models.ForeignKey(CallResponses, on_delete=models.CASCADE, null=True)
    sales = models.ForeignKey(SalesTeamDetails, on_delete=models.CASCADE, null=True, blank=True)
    note = models.TextField(blank=True, null=True)
    date = models.DateField()

    class Meta:
        unique_together = ['customer', 'date']
