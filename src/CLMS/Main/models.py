from django.db import models
from image_cropping import ImageRatioField
from django.contrib import admin
from django import forms
# Create your models here.


class Tag(models.Model):
    name = models.CharField(max_length=20)

    def __str__(self):
        return self.name


class Competition(models.Model):
    title = models.CharField(max_length=100)
    subtitle = models.CharField(max_length=100, blank=True, null=True)

    # basic info
    hold_time = models.DateTimeField()
    holder = models.CharField(max_length=100)
    state = models.CharField(max_length=100)

    # text
    intro = models.TextField(blank=True, null=True)
    content = models.TextField(blank=True, null=True)
    method = models.TextField(blank=True, null=True)
    award = models.TextField(blank=True, null=True)

    # image
    image = models.ImageField(
        upload_to='./media/Competition/images/', null=True, blank=True)
    cropping = ImageRatioField('image', '640x480')

    tag = models.ManyToManyField(Tag)

    # what is this?
    likes = models.IntegerField(default=0)
    views = models.IntegerField(default=0)

    result = models.FileField(
        upload_to='./Competition/result/', null=True, blank=True)

    date_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['-date_time']


class Lecture(models.Model):
    title = models.CharField(max_length=100)
    subtitle = models.CharField(max_length=100, blank=True, null=True)

    # basic info
    hold_time = models.DateTimeField()
    holder = models.CharField(max_length=100)
    state = models.CharField(max_length=100)

    # text
    intro = models.TextField(blank=True, null=True)
    content = models.TextField(blank=True, null=True)
    news = models.TextField(blank=True, null=True)

    likes = models.IntegerField(default=0)
    views = models.IntegerField(default=0)

    # image
    image = models.ImageField(
        upload_to='./media/Lecture/images/', null=True, blank=True)
    cropping = ImageRatioField('image', '640x480')

    tag = models.ManyToManyField(Tag)

    date_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['-date_time']


class User(models.Model):
    username = models.CharField(max_length=30)
    password = models.CharField(max_length=30)

    def __unicode__(self):
        return self.username

