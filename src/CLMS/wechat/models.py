from django.db import models
# from Main.models import Tag
# from image_cropping import ImageRatioField
# from django.db.models.fields.files import ImageFieldFile
# import os
# # from django.contrib.auth.models import AbstractUser
# # # Create your models here.

# # class Users(AbstractUser):
# # 	openid = models.CharField(max_length=100,blank=True,null=True,verbose_name="openid",unique=True)
# class WechatUser(models.Model):
# 	'''tagInterest = (
#         ('Science',(
#             ('Program','Programming'),
#             ('HardWare','Hardware'),
#             ('Arch','Building'),
#             )
#         ),
#         ('Humanity',(
#             ('Poem','Poems'),
#             ('Comp','Composition'),
#             )
#         ),
#     )'''
# 	open_id = models.CharField(max_length=50)
# 	tagInterest = models.ManyToManyField(Tag, blank=True)   # for recommendation
# 	def __unicode__(self):
#         return self.openid