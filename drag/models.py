
from django.db import models
from django.utils import timezone


class Category(models.Model):
    name = models.CharField(max_length=100 ,null=True, blank=True)
    margin = models.CharField(max_length=100 ,null=True, blank=True)

    def __str__(self):
        return self.name

class Customer(models.Model):
    name = models.CharField(max_length=100)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class Freight_Rate(models.Model):
    POL = models.CharField(max_length=100,null=True, blank=True)
    POD = models.CharField(max_length=100,null=True, blank=True)
    LINER = models.CharField(max_length=100,null=True, blank=True)
    TYPE = models.CharField(max_length=100,null=True, blank=True)
    THC = models.CharField(max_length=100,null=True, blank=True)
    field6 = models.CharField(max_length=100,null=True, blank=True)
    CONTAINER = models.CharField(max_length=100,null=True, blank=True)
    field8 = models.CharField(max_length=100,null=True, blank=True)
    CONTAINER_PRICE = models.CharField(max_length=100,null=True, blank=True)
    SAEL_AMOUNT = models.CharField(max_length=100,null=True, blank=True)
    FREE_FEE = models.CharField(max_length=100,null=True, blank=True)
    FREE_DAYS = models.CharField(max_length=100,null=True, blank=True)
    VALIDITY_FROM = models.CharField(max_length=100,null=True, blank=True)
    VALIDITY_TO = models.CharField(max_length=100,null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True,null=True, blank=True)

    def has_expired(self):
        """
        Check if the record has expired based on its date field.
        """
        current_date = datetime.now().date()
        # Convert self.date to datetime.date object if it's stored as a string
        record_date = datetime.strptime(self.date, '%d-%m-%Y').date() if isinstance(self.date, str) else self.date
        return record_date < current_date

class Customercategory(models.Model):
    id = models.BigAutoField(db_column='Id', primary_key=True)  # Field name made lowercase.
    categorynameeng = models.CharField(db_column='CategoryNameEng', max_length=100)  # Field name made lowercase.
    categorynamejpn = models.CharField(db_column='CategoryNameJpn', max_length=255)  # Field name made lowercase.
    margin = models.IntegerField(db_column='Margin', blank=True, null=True)  # Field name made lowercase.
    createddatetimeutc = models.DateTimeField(db_column='CreatedDateTimeUtc')  # Field name made lowercase.
    createdby = models.CharField(db_column='CreatedBy', max_length=250)  # Field name made lowercase.
    updateddatetimeutc = models.DateTimeField(db_column='UpdatedDateTimeUtc')  # Field name made lowercase.
    updatedby = models.CharField(db_column='UpdatedBy', max_length=250)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'CustomerCategory'

class Country(models.Model):
    id = models.BigAutoField(db_column='Id', primary_key=True)  # Field name made lowercase.
    countrynameeng = models.CharField(db_column='CountryNameEng', max_length=255, blank=True, null=True)  # Field name made lowercase.
    countrynamejpn = models.CharField(db_column='CountryNameJpn', max_length=255, blank=True, null=True)  # Field name made lowercase.
    uppercode = models.CharField(db_column='UpperCode', max_length=255, blank=True, null=True)  # Field name made lowercase.
    lowercode = models.CharField(db_column='LowerCode', max_length=255, blank=True, null=True)  # Field name made lowercase.
    nacsscountryid = models.CharField(db_column='NacssCountryId', max_length=2, blank=True, null=True)  # Field name made lowercase.
    uncode = models.CharField(db_column='UnCode', max_length=10, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Country'

class Customercompany(models.Model):
    id = models.BigAutoField(db_column='Id', primary_key=True)  # Field name made lowercase.
    companycountryid = models.ForeignKey(Country, models.CASCADE, db_column='CompanyCountryId')  # Field name made lowercase.
    companynameeng = models.CharField(db_column='CompanyNameEng', unique=True, max_length=100)  # Field name made lowercase.
    companynamejpn = models.CharField(db_column='CompanyNameJpn', unique=True, max_length=255)  # Field name made lowercase.
    primarypepresentative = models.CharField(db_column='PrimaryPepresentative', max_length=100)  # Field name made lowercase.
    secondarypepresentative = models.CharField(db_column='SecondaryPepresentative', max_length=100, blank=True, null=True)  # Field name made lowercase.
    officepostbox = models.CharField(db_column='OfficePostBox', max_length=20)  # Field name made lowercase.
    officeprefectureeng = models.CharField(db_column='OfficePrefectureEng', max_length=100)  # Field name made lowercase.
    officeprefecturejpn = models.CharField(db_column='OfficePrefectureJpn', max_length=100)  # Field name made lowercase.
    officecityeng = models.CharField(db_column='OfficeCityEng', max_length=100)  # Field name made lowercase.
    officecityjpn = models.CharField(db_column='OfficeCityJpn', max_length=100)  # Field name made lowercase.
    officeaddresseng = models.CharField(db_column='OfficeAddressEng', max_length=500)  # Field name made lowercase.
    officeaddressjpn = models.CharField(db_column='OfficeAddressJpn', max_length=500)  # Field name made lowercase.
    officephone = models.CharField(db_column='OfficePhone', unique=True, max_length=255)  # Field name made lowercase.
    officefax = models.CharField(db_column='OfficeFax', unique=True, max_length=255)  # Field name made lowercase.
    custompostbox = models.CharField(db_column='CustomPostBox', max_length=20)  # Field name made lowercase.
    customprefectureeng = models.CharField(db_column='CustomPrefectureEng', max_length=100)  # Field name made lowercase.
    customprefecturejpn = models.CharField(db_column='CustomPrefectureJpn', max_length=100)  # Field name made lowercase.
    customcityeng = models.CharField(db_column='CustomCityEng', max_length=100)  # Field name made lowercase.
    customcityjpn = models.CharField(db_column='CustomCityJpn', max_length=100)  # Field name made lowercase.
    customaddresseng = models.CharField(db_column='CustomAddressEng', max_length=500)  # Field name made lowercase.
    customaddressjpn = models.CharField(db_column='CustomAddressJpn', max_length=500)  # Field name made lowercase.
    iecode = models.CharField(db_column='IECode', max_length=100, blank=True, null=True)  # Field name made lowercase.
    mailingpostbox = models.CharField(db_column='MailingPostBox', max_length=20)  # Field name made lowercase.
    mailingprefectureeng = models.CharField(db_column='MailingPrefectureEng', max_length=100)  # Field name made lowercase.
    mailingprefecturejpn = models.CharField(db_column='MailingPrefectureJpn', max_length=100)  # Field name made lowercase.
    mailingcityeng = models.CharField(db_column='MailingCityEng', max_length=100)  # Field name made lowercase.
    mailingcityjpn = models.CharField(db_column='MailingCityJpn', max_length=100)  # Field name made lowercase.
    mailingaddresseng = models.CharField(db_column='MailingAddressEng', max_length=500)  # Field name made lowercase.
    mailingaddressjpn = models.CharField(db_column='MailingAddressJpn', max_length=500)  # Field name made lowercase.
    companyremarks = models.TextField(db_column='CompanyRemarks', blank=True, null=True)  # Field name made lowercase.
    picturestoclick = models.CharField(db_column='PicturesToClick', max_length=250)  # Field name made lowercase.
    status = models.CharField(db_column='Status', max_length=20)  # Field name made lowercase.
    createddatetimeutc = models.DateTimeField(db_column='CreatedDateTimeUtc')  # Field name made lowercase.
    createdby = models.CharField(db_column='CreatedBy', max_length=250)  # Field name made lowercase.
    updateddatetimeutc = models.DateTimeField(db_column='UpdatedDateTimeUtc')  # Field name made lowercase.
    updatedby = models.CharField(db_column='UpdatedBy', max_length=250)  # Field name made lowercase.
    customercategoryid = models.ForeignKey(Customercategory, models.CASCADE, db_column='CustomerCategoryId')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'CustomerCompany'

class Port(models.Model):
    id = models.BigAutoField(db_column='Id', primary_key=True)  # Field name made lowercase.
    portnameeng = models.CharField(db_column='PortNameEng', unique=True, max_length=100)  # Field name made lowercase.
    portnamejpn = models.CharField(db_column='PortNameJpn', unique=True, max_length=100)  # Field name made lowercase.
    portcountryid = models.ForeignKey('Country', models.DO_NOTHING, db_column='PortCountryId')  # Field name made lowercase.
    naccsportcode = models.CharField(db_column='NaccsPortCode', max_length=10, blank=True, null=True)  # Field name made lowercase.
    naccsstandardcode = models.CharField(db_column='NaccsStandardCode', max_length=20, blank=True, null=True)  # Field name made lowercase.
    inttraportcode = models.CharField(db_column='InttraPortCode', max_length=255, blank=True, null=True)  # Field name made lowercase.
    createddatetimeutc = models.DateTimeField(db_column='CreatedDateTimeUtc')  # Field name made lowercase.
    createdby = models.CharField(db_column='CreatedBy', max_length=250)  # Field name made lowercase.
    updateddatetimeutc = models.DateTimeField(db_column='UpdatedDateTimeUtc')  # Field name made lowercase.
    updatedby = models.CharField(db_column='UpdatedBy', max_length=250)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Port'

class Shippingcontainersize(models.Model):
    id = models.BigAutoField(db_column='Id', primary_key=True)  # Field name made lowercase.
    size = models.CharField(db_column='Size', max_length=30)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Shippingcontainersize'

class Shippingcompany(models.Model):
    id = models.BigAutoField(db_column='Id', primary_key=True)  # Field name made lowercase.
    companynameeng = models.CharField(db_column='CompanyNameEng', max_length=255)  # Field name made lowercase.
    companynamejpn = models.CharField(db_column='CompanyNameJpn', max_length=255)  # Field name made lowercase.
    postbox = models.CharField(db_column='PostBox', max_length=20, blank=True, null=True)  # Field name made lowercase.
    prefectureeng = models.CharField(db_column='PrefectureEng', max_length=100, blank=True, null=True)  # Field name made lowercase.
    prefecturejpn = models.CharField(db_column='PrefectureJpn', max_length=100, blank=True, null=True)  # Field name made lowercase.
    cityeng = models.CharField(db_column='CityEng', max_length=100, blank=True, null=True)  # Field name made lowercase.
    cityjpn = models.CharField(db_column='CityJpn', max_length=100, blank=True, null=True)  # Field name made lowercase.
    addresseng = models.CharField(db_column='AddressEng', max_length=500, blank=True, null=True)  # Field name made lowercase.
    addressjpn = models.CharField(db_column='AddressJpn', max_length=500, blank=True, null=True)  # Field name made lowercase.
    bllatepickfeebasedatetype = models.CharField(db_column='BLLatePickFeeBaseDateType', max_length=10)  # Field name made lowercase.
    bllatepickfeebeforeafter = models.CharField(db_column='BLLatePickFeeBeforeAfter', max_length=10)  # Field name made lowercase.
    bllatepickfeeperioddays = models.IntegerField(db_column='BLLatePickFeePeriodDays')  # Field name made lowercase.
    bllatepickfeeprice = models.IntegerField(db_column='BLLatePickFeePrice')  # Field name made lowercase.
    bllatepickfeetaxpercetage = models.IntegerField(db_column='BLLatePickFeeTaxPercetage')  # Field name made lowercase.
    naccscode = models.CharField(db_column='NaccsCode', max_length=25, blank=True, null=True)  # Field name made lowercase.
    inttracode = models.CharField(db_column='InttraCode', max_length=35, blank=True, null=True)  # Field name made lowercase.
    createddatetimeutc = models.DateTimeField(db_column='CreatedDateTimeUtc')  # Field name made lowercase.
    createdby = models.CharField(db_column='CreatedBy', max_length=250)  # Field name made lowercase.
    updatedatetimeutc = models.DateTimeField(db_column='UpdateDateTimeUtc')  # Field name made lowercase.
    updatedby = models.CharField(db_column='UpdatedBy', max_length=250)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Shippingcompany'


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

from datetime import datetime
class Freightrate(models.Model):
    id = models.BigAutoField(primary_key=True, db_column='Id')
    polid = models.ForeignKey('Port', models.DO_NOTHING, db_column='PolId')  # Field name made lowercase.
    podid = models.ForeignKey('Port', models.DO_NOTHING, db_column='PodId', related_name='freightrate_podid_set')  # Field name made lowercase.
    shippingcompanyid = models.ForeignKey('Shippingcompany', models.DO_NOTHING, db_column='ShippingCompanyId')  # Field name made lowercase.
    shippingcontainersizeid = models.ForeignKey('Shippingcontainersize', models.DO_NOTHING, db_column='ShippingContainerSizeId')  # Field name made lowercase.
    currencyid = models.ForeignKey('Currencymst', models.DO_NOTHING, db_column='CurrencyId',blank=True, null=True)  # Field name made lowercase.
    sealamount = models.DecimalField(db_column='SealAmount', max_digits=18, decimal_places=0, blank=True, null=True)  # Field name made lowercase.
    oceanfreight = models.DecimalField(db_column='OceanFreight', max_digits=18, decimal_places=0)  # Field name made lowercase.
    docfee = models.DecimalField(db_column='DocFee', max_digits=18, decimal_places=0, blank=True, null=True)  # Field name made lowercase.
    thc = models.IntegerField(db_column='THC')  # Field name made lowercase.
    type = models.CharField(db_column='Type', max_length=15, blank=True, null=True)  # Field name made lowercase.
    freedays = models.IntegerField(db_column='FreeDays', blank=True, null=True)  # Field name made lowercase.
    validityfrom = models.DateTimeField(db_column='ValidityFrom', blank=True, null=True)  # Field name made lowercase.
    validityto = models.DateTimeField(db_column='ValidityTo', blank=True, null=True)  # Field name made lowercase.
    createddatetimeutc = models.DateTimeField(db_column='CreatedDateTimeUtc',default=datetime.utcnow)  # Field name made lowercase.
    createdby = models.CharField(db_column='CreatedBy', max_length=250)  # Field name made lowercase.
    updateddatetimeutc = models.DateTimeField(db_column='UpdatedDateTimeUtc',default=datetime.utcnow)  # Field name made lowercase.
    updatedby = models.CharField(db_column='UpdatedBy', max_length=250)  # Field name made lowercase.


    def has_expired(self):
        """
        Check if the record has expired based on its date field.
        """
        current_date = datetime.now().date()
        # Convert self.date to datetime.date object if it's stored as a string
        record_date = datetime.strptime(self.date, '%d-%m-%Y').date() if isinstance(self.date, str) else self.date
        return record_date < current_date

    class Meta:
        managed = False
        db_table = 'FreightRate'


