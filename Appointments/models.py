from django.db import models
from Accounts.models import CustomerDetails, DoctorDetails
from datetime import datetime


class Appointments(models.Model):
    doctor = models.ForeignKey(DoctorDetails, on_delete=models.CASCADE, null=True)
    customer = models.ForeignKey(CustomerDetails, on_delete=models.CASCADE , related_name="customer_appointments")
    date = models.DateField()
    time = models.TimeField()
    schedule = models.DateTimeField(default=datetime.now)
    approved = models.BooleanField(default=False)
    rejected = models.BooleanField(default=False)
    rescheduled_by_doctor = models.BooleanField(default=False)
    rescheduled_by_client = models.BooleanField(default=False)
    completed = models.BooleanField(default=False)
    meeting_url = models.URLField(null=True)
    is_rescheduled = models.BooleanField(default=False)

    is_paid = models.BooleanField(default=False)
    uid = models.CharField(max_length=100 , null=True , blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    # class Meta:
    #     unique_together = ['date', 'customer', 'doctor', 'approved']


    def __str__(self):
        return self.customer.user.firstname


class AppointmentSummary(models.Model):
    appointment = models.ForeignKey(Appointments, on_delete=models.CASCADE)
    summary = models.TextField()
