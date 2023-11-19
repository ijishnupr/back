# Generated by Django 4.2.6 on 2023-11-05 10:29

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Accounts', '0003_alter_user_role'),
    ]

    operations = [
        migrations.CreateModel(
            name='SalesTeamDetails',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('location', models.CharField(blank=True, max_length=200, null=True)),
                ('passwordString', models.CharField(max_length=500)),
                ('user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='salesDetails', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]