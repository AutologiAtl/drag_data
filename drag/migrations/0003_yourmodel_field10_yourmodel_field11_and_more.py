# Generated by Django 5.0.4 on 2024-04-24 11:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('drag', '0002_yourmodel'),
    ]

    operations = [
        migrations.AddField(
            model_name='yourmodel',
            name='field10',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='yourmodel',
            name='field11',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='yourmodel',
            name='field12',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='yourmodel',
            name='field3',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='yourmodel',
            name='field4',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='yourmodel',
            name='field5',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='yourmodel',
            name='field6',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='yourmodel',
            name='field7',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='yourmodel',
            name='field8',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='yourmodel',
            name='field9',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='yourmodel',
            name='field1',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='yourmodel',
            name='field2',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
    ]
