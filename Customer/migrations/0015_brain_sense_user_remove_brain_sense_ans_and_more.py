# Generated by Django 4.2.7 on 2023-12-18 13:40

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('Customer', '0014_alter_vaccination_user_date_brain_visual_brain_sense'),
    ]

    operations = [
        migrations.CreateModel(
            name='Brain_sense_user',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
        ),
        migrations.RemoveField(
            model_name='brain_sense',
            name='ans',
        ),
        migrations.RemoveField(
            model_name='brain_sense',
            name='user',
        ),
        migrations.DeleteModel(
            name='Brain_visual',
        ),
        migrations.AddField(
            model_name='brain_sense_user',
            name='sense',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Customer.brain_sense'),
        ),
        migrations.AddField(
            model_name='brain_sense_user',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
