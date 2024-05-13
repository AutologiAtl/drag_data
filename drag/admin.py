from django.contrib import admin

# Register your models here.

from drag.models import *
admin.site.register(Category)
admin.site.register(Customer)
admin.site.register(Freight_Rate)
admin.site.register(Freightrate)