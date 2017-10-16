from django.contrib import admin
from Main import models as models
# Register your models here.

admin.site.register(models.Tag)
admin.site.register(models.Competition)
admin.site.register(models.Lecture)
