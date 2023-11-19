# Generated by Django 3.2.4 on 2021-06-24 09:24

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('LearnIt', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Videos',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('video', models.FileField(blank=True, null=True, upload_to='videos/')),
                ('url', models.URLField(blank=True, null=True)),
                ('module', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='LearnIt.modules')),
                ('stage', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='LearnIt.stage')),
            ],
        ),
    ]
