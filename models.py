# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class Currencymst(models.Model):
    id = models.BigIntegerField(db_column='Id', primary_key=True)  # Field name made lowercase.
    createddatetimeutc = models.DateTimeField(db_column='CreatedDateTimeUtc')  # Field name made lowercase.
    createdby = models.CharField(db_column='CreatedBy', max_length=250)  # Field name made lowercase.
    updateddatetimeutc = models.DateTimeField(db_column='UpdatedDateTimeUtc')  # Field name made lowercase.
    updatedby = models.CharField(db_column='UpdatedBy', max_length=250)  # Field name made lowercase.
    currencydesc = models.CharField(db_column='CurrencyDesc', max_length=100, blank=True, null=True)  # Field name made lowercase.
    currencysymbol = models.CharField(db_column='CurrencySymbol', max_length=2000, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Currencymst'
