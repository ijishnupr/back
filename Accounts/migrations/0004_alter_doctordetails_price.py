# Generated by Django 3.2.4 on 2024-05-28 00:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Accounts', '0003_plans'),
    ]

    operations = [
        migrations.AlterField(
            model_name='doctordetails',
            name='price',
            field=models.IntegerField(default=10),
        ),
    ]
