"""dasha URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
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

from dasha import views

urlpatterns = [
    url(r'^$', views.IndexView.as_view(), name='index'),
    url(r'^login/$', views.AuthView.as_view()),
    # url(r'^logout/$')
    url(r'^add_news/$', views.NewsAdd.as_view(), name='add_news'),
    url(r'^add_tm/$', views.TMAdd.as_view(), name='add_tm'),
    url(r'^edit_tm/(?P<id>\d+)/$', views.TMEdit.as_view(), name='edit_tm'),
    url(r'^edit_news/(?P<id>\d+)/$', views.NewsEdit.as_view(), name='edit_news'),
    url(r'^answer/(?P<id>\d+)/$', views.AddAnswer.as_view(), name='add_answer'),
    url(r'remove/news/(?P<id>\d+)/$', views.NewsDelete.as_view(), name='delete_news'),
    url(r'remove/tm/(?P<id>\d+)/$', views.TMDelete.as_view(), name='delete_tm')
]
