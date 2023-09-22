from django.contrib import admin

from . import models 

# Register your models here.

admin.site.register(models.Entrepreneurs)
admin.site.register(models.Registrations)
admin.site.register(models.Transactions)
admin.site.register(models.Investors)