from django.contrib import admin
from . models import *
# Register your models here.
models = [Brand, Product]
admin.site.register(models)