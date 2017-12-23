from django.db import models
from image_cropping import ImageRatioField
from django.db.models.fields.files import ImageFieldFile
import os

from Main.utils import make_thumb


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

    # admin info
    adminUser = models.CharField(max_length=50, blank=True)

    # text
    intro = models.TextField(blank=True, null=True)
    content = models.TextField(blank=True, null=True)
    method = models.TextField(blank=True, null=True)
    award = models.TextField(blank=True, null=True)

    # image
    image = models.ImageField(
        upload_to='./Competition/images/', null=True, blank=True)
    thumb = models.ImageField(upload_to='./Competition/thumbs', blank=True)
    cropping = ImageRatioField('image', '640x480')

    tag = models.ManyToManyField(Tag, blank=True)

    # what is this?
    likes = models.IntegerField(default=0)
    views = models.IntegerField(default=0)

    result = models.FileField(
        upload_to='./Competition/result/', null=True, blank=True)

    date_time = models.DateTimeField(auto_now_add=True)

    adminUser = models.CharField(max_length=30)

    def save(self):
        super(Competition, self).save()
        # base, ext = os.path.splitext(os.path.basename(self.image.path))
        thumb_path = os.path.join(
            './media/Competition/thumbs/', os.path.basename(self.image.path))
        make_thumb(self.image.path, thumb_path)

        # thumb_path = os.path.join(MEDIA_ROOT, relate_thumb_path)
        thumb_path = os.path.join(
            './Competition/thumbs/', os.path.basename(self.image.path))
        self.thumb = ImageFieldFile(self, self.thumb, thumb_path)
        super(Competition, self).save()
        
    '''def update(self):
        super(Competition, self).update()
        # base, ext = os.path.splitext(os.path.basename(self.image.path))
        thumb_path = os.path.join(
            './media/Competition/thumbs/', os.path.basename(self.image.path))
        make_thumb(self.image.path, thumb_path)
        # thumb_path = os.path.join(MEDIA_ROOT, relate_thumb_path)
        thumb_path = os.path.join(
            './Competition/thumbs/', os.path.basename(self.image.path))
        self.thumb = ImageFieldFile(self, self.thumb, thumb_path)
        super(Competition, self).save()'''

        
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

    # admin info
    adminUser = models.CharField(max_length=30)

    # text
    intro = models.TextField(blank=True, null=True)
    content = models.TextField(blank=True, null=True)
    news = models.TextField(blank=True, null=True)

    likes = models.IntegerField(default=0)
    views = models.IntegerField(default=0)

    # image
    image = models.ImageField(
        upload_to='./Lecture/images/', null=True, blank=True)
    thumb = models.ImageField(upload_to='./Lecture/thumbs', blank=True)
    cropping = ImageRatioField('image', '640x480')

    tag = models.ManyToManyField(Tag, blank=True)

    date_time = models.DateTimeField(auto_now_add=True)

    def save(self):
        super(Lecture, self).save()
        # base, ext = os.path.splitext(os.path.basename(self.image.path))
        thumb_path = os.path.join(
            './media/Lecture/thumbs/', os.path.basename(self.image.path))
        print(self.image.path)
        make_thumb(self.image.path, thumb_path)

        # thumb_path = os.path.join(MEDIA_ROOT, relate_thumb_path)
        thumb_path = os.path.join(
            './Lecture/thumbs/', os.path.basename(self.image.path))
        self.thumb = ImageFieldFile(self, self.thumb, thumb_path)
        super(Lecture, self).save()

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['-date_time']


class User(models.Model):

    '''tagInterest = (
        ('Science',(
            ('Program','Programming'),
            ('HardWare','Hardware'),
            ('Arch','Building'),
            )
        ),
        ('Humanity',(
            ('Poem','Poems'),
            ('Comp','Composition'),
            )
        ),
    )'''

    username = models.CharField(max_length=30)
    password = models.CharField(max_length=50)

    # Undergraduate or graduate student
    stuType = models.CharField(max_length=30, blank=True)
    infoUser = models.CharField(max_length=30, blank=True)
    infoPasswd = models.CharField(max_length=30, blank=True)
    infoValid = models.BooleanField(default=False)
    email = models.EmailField(max_length=40, blank=True)
    emailValid = models.BooleanField(default=False)
    stuName = models.CharField(max_length=15, blank=True)
    stuNo = models.IntegerField(default=2000000000)
    grade = models.CharField(max_length=20, default='-------')
    interestTag = models.ManyToManyField(
        Tag, blank=True)   # for recommendation
    adminAuth = models.BooleanField(default=True)

    # The competitons and lectures user like
    CompetitionList = models.ManyToManyField(Competition, blank=True,null=True)
    LectureList = models.ManyToManyField(Lecture,blank=True,null=True)
    #adminAuth = models.BooleanField(default=False)

    def __unicode__(self):
        return self.username

# for wechat user
class wechatUser(models.Model):
    openid = models.CharField(max_length=50)
    
    #link wechat user to the main user and check whether the account is valid
    #in case we need to link it to another account :-)
    mainUser = models.OneToOneField(User, primary_key=True)
    userLink = models.BooleanField(default=False)
    
class identifyCode(models.Model):
    idenCode = models.CharField(max_length=10)
    openid = models.CharField(max_length=50)
    