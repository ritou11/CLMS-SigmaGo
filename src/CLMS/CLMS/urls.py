"""CLMS URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin
from Main import views
from django.conf import settings
from django.conf.urls.static import static
#from wechat.menu.view import refresh as refresh_menu
from wechat.actions.view import all_actions as refresh_actions
from xadmin.plugins import xversion
import xadmin
xadmin.autodiscover()


xversion.register_models()

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^$', views.home, name='home'),
    url(r'^Competition/(?P<id>\d+)/$', views.competition, name='Competition'),
    url(r'^Lecture/(?P<id>\d+)/$', views.lecture, name='Lecture'),
    url(r'^Slide/(?P<id>\d+)/$', views.slide, name='Slide'),
    url(r'^CompetitionList/$', views.competitionList, name='CompetitionList'),
    url(r'^LectureList/$', views.lectureList, name='LectureList'),
    url(r'^tag(?P<tag>\w+)/$',views.search_tag,name='search_tag'),
    url(r'^search/$',views.search,name='search'),

    url(r'^index/$', views.index, name='index4test'),
    url(r'^login/$', views.login, name='Login'),
    url(r'^register/$', views.register, name='Register'),
    
    #url(r'^refresh_menu/', refresh_menu),
    url(r'^refresh_actions/', refresh_actions),
    #url(r'^refresh_user/', refresh_user),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
