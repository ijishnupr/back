# Generated by Django 4.2.7 on 2023-12-27 08:38

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Doctor', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='appointmentsummary',
            name='appointment',
        ),
        migrations.DeleteModel(
            name='Appointments',
        ),
        migrations.DeleteModel(
            name='AppointmentSummary',
        ),
    ]
