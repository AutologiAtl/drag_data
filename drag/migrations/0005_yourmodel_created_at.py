# Generated by Django 5.0.4 on 2024-05-01 04:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('drag', '0004_yourmodel_field13_yourmodel_field14'),
    ]

    operations = [
        migrations.AddField(
            model_name='yourmodel',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, null=True),
        ),
    ]
