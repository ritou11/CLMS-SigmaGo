from django.db import models

# Create your models here.


class Tag(models.Model):
    name = models.CharField(max_length=20)

    def __str__(self):
        return self.name


class Competition(models.Model):
    title = models.CharField(max_length=100)
    date_time = models.DateTimeField(auto_now_add=True)
    holder = models.CharField(max_length=100)
    intro = models.TextField(blank=True, null=True)
    content = models.TextField(blank=True, null=True)
    method = models.TextField(blank=True, null=True)
    award = models.TextField(blank=True, null=True)
    image = models.ImageField(
        upload_to='./Competition/images/', null=True, blank=True)
    tag = models.ManyToManyField(Tag)
    result = models.FileField(
        upload_to='./Competition/result/', null=True, blank=True)

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['-date_time']


class Lecture(models.Model):
    title = models.CharField(max_length=100)
    date_time = models.DateTimeField(auto_now_add=True)
    intro = models.TextField(blank=True, null=True)
    content = models.TextField(blank=True, null=True)
    news = models.TextField(blank=True, null=True)
    image = models.ImageField(
        upload_to='./Lecture/images/', null=True, blank=True)
    tag = models.ManyToManyField(Tag)

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['-date_time']
