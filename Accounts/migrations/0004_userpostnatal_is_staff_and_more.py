# Generated by Django 4.2.6 on 2023-10-29 20:55

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('Accounts', '0003_rename_date_of_birth_customerdetails_date_of_birth_parent_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='userpostnatal',
            name='is_staff',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='userpostnatal',
            name='dateJoined',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
        migrations.AlterField(
            model_name='userpostnatal',
            name='firstname',
            field=models.CharField(default='firstname', max_length=100),
        ),
        migrations.AlterField(
            model_name='userpostnatal',
            name='lastname',
            field=models.CharField(max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='userpostnatal',
            name='role',
            field=models.CharField(choices=[('client', 'Client'), ('doctor', 'Doctor'), ('sales', 'Sales'), ('admin', 'Admin')], default='client', max_length=10),
        ),
    ]