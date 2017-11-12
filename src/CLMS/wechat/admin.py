#from django.contrib import admin
import xadmin
from .models import Menu, Actions

# Register your models here.


class MenuAdmin(object):
    list_display = ('id', 'count', 'modify_time')
    search_fields = ('id', 'count', 'modify_time', 'info')
    
    
class ActionAdmin(object):
    list_display = ('id', 'action_name', 'description', "level", "rule", 'action_type')
    search_fields = ('id', 'action_name', 'description', "level", "rule", 'action_type')
    
    

xadmin.site.register(Menu, MenuAdmin)
xadmin.site.register(Actions, ActionAdmin)
