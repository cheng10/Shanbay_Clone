"""Shanbay_Clone URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.9/topics/http/urls/
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
from django.conf.urls import url, include
from django.contrib import admin
# rest_api
from rest_framework import routers
from rest_api import views

router = routers.DefaultRouter()
router.register(r'users', views.UserViewSet)
router.register(r'groups', views.GroupViewSet)
router.register(r'learners', views.LearnerViewSet)
router.register(r'word', views.WordViewSet)
router.register(r'book', views.BookViewSet)
router.register(r'knownWords', views.KnowWordsViewSet)
router.register(r'levelWord', views.LevelWordViewSet)
router.register(r'learningWords', views.LearningWordsViewSet)

urlpatterns = [
    url(r'^$', 'words.views.home', name='home'),
    url(r'^admin/', admin.site.urls),
    url(r'^words/', 'words.views.words', name='words'),
    url(r'^bdc/', 'words.views.bdc', name='bdc'),
    url(r'^about/', 'words.views.about', name='about'),
    # url(r'^word/(?P<id>\d+)/$', 'words.views.detail', name='detail'),
    url(r'^word/(?P<word_name>[a-zA-Z]+)/$', 'words.views.word_detail', name='word_detail'),
    url(r'^signup/$', 'words.views.register', name='signup'),
    url(r'^login/$', 'words.views.user_login', name='login'),
    url(r'^logout/$', 'words.views.user_logout', name='logout'),
    url(r'^restricted/', 'words.views.restricted', name='restricted'),
    # rest_api
    url(r'^api/', include(router.urls)),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework'))
]
