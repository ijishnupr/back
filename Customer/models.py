from django.db import models
from django.db.models.fields import DateField, DateTimeField
from django.contrib.auth import get_user_model
User = get_user_model()


from enum import unique
from faulthandler import disable
from logging import critical
from re import S
from django.db import models
from datetime import datetime
from django.db.models.fields import DateField, DateTimeField
from django.utils.timezone import make_aware
from django.utils.timezone import now
from LearnIt.models import Stage

from django.contrib.auth import get_user_model
User = get_user_model()

# Create your models here.


class MedicineTime(models.Model):
    name = models.CharField(max_length=100, null=True, unique=True)
    

    def __str__(self):
        return self.name
    class Meta:
        verbose_name = 'Medicine time(manual)'


#med by client
class Medicines(models.Model):
    date = DateField(auto_now_add=True)
    customer = models.ForeignKey(User, on_delete=models.CASCADE)
    time = models.ForeignKey(MedicineTime, on_delete=models.CASCADE, related_name="Medicines") 
    name = models.CharField(max_length=300, null=True)

    # def __str__(self):
    #     return self.name

    class Meta:
        unique_together = ['customer', 'time', 'name']



class LastUpdateDate(models.Model):
    date = datetime.now()
    timezone_aware_date = make_aware(date)
    customer = models.ForeignKey(User, on_delete=models.CASCADE, related_name="last_update")
    # diet = models.DateTimeField(default=now)
    medicine = models.DateTimeField(default=now)
    # activity = models.DateTimeField(default=now)
    # symptom = models.DateTimeField(default=now)
    # exercise = models.DateTimeField(default=now)
    # contraction = models.DateTimeField(default=now)

    def __str__(self):
        return self.customer.email
    

class TakenMedicine(models.Model):
    medicine = models.ForeignKey(Medicines, on_delete=models.CASCADE, related_name='MedicineDetail', null=True)
    customer = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    date = models.DateField()
    taken = models.BooleanField(default=False)

    class Meta:
        ordering = ['-date']
        unique_together = ['medicine', 'customer', 'date']



class BreastfeedingRecord(models.Model):
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, related_name='breastfeeding_records')
    date = models.DateField()
    feeding_number = models.PositiveSmallIntegerField()
    is_breastfed = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.user} - {self.date} - Feeding {self.feeding_number}: {self.is_breastfed}"