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
from wechat.views import wechat


urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^$', views.home, name='home'),
    url(r'^competition/(?P<id>\d+)/$', views.competition, name='Competition'),
    url(r'^lecture/(?P<id>\d+)/$', views.lecture, name='Lecture'),
    url(r'^competition-list/(?P<page>\d*)$',
        views.competitionList, name='CompetitionList'),
    url(r'^lecture-list/(?P<page>\d*)$', views.lectureList, name='LectureList'),
    url(r'^tag/(?P<tag>\w+)/(?P<page>\d*)$', views.search_tag, name='search_tag'),
    url(r'^search/$', views.search, name='search'),
    url(r'^recom/(?P<page>\d*)$', views.recommend, name='recommend'),
    url(r'^like$', views.like, name='like'),
    url(r'^tag-api$', views.tag_api, name='tag_api'),
    url(r'^index$', views.home, name='home'),
    url(r'^login/$', views.login, name='Login'),
    url(r'^logout/$', views.logout, name='Logout'),
    url(r'^register/$', views.register, name='Register'),
    url(r'^userinfo/$', views.userInfoSearch, name='UserInfoSearch'),
    url(r'^infocheck/inforenew/$', views.userInfoAlter, name='InfoRenew'),
    url(r'^conAdd/$', views.contestAdd, name='contestInfo'),
    url(r'^lecAdd/$', views.lectureAdd, name='lectureInfo'),
    url(r'^manage/$', views.lecConManagement, name='adminmanage'),
    url(r'^comtetitionManage/(\d+)/$', views.competitionManagement, name='adminmanage'),
    url(r'^lectureManage/(\d+)/$', views.lectureManagement, name='adminmanage'),
    url(r'^weixin', wechat, name='weixin'),
    # url(r'^wechat$', views.wechat, name='Wechat')
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
