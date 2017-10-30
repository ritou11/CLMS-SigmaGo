from django.contrib import admin
from Main import models as models
from image_cropping import ImageCroppingMixin
# Register your models here.

class MyModelAdmin(ImageCroppingMixin,admin.ModelAdmin):
    pass

admin.site.register(models.Tag)
admin.site.register(models.Competition)
admin.site.register(models.Lecture)
