# Generated by Django 5.1.7 on 2025-05-26 17:33

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0002_post_solution'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='community',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='posts', to='dashboard.study_group'),
        ),
    ]
