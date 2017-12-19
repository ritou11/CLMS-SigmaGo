# from .models import Users
# '''
# 	wechat auth
# '''

# class WeChatOpenIdAuth(object):
# 	def get_user(self, id_):
# 		try:
# 			return Users.objects.get(pk=id_)
# 		except Users.DoesNotExist:
# 			return None

# 	def authenticate(self, openid=None):
# 		try:
# 			user = Users.objects.get(openid=openid)
# 			if user is not None:
# 				return user
# 			return None
# 		except Users.DoesNotExist:
# 			return None
