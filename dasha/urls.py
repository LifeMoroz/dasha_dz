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
    url(r'^$', views.NewsList.as_view(), name='news-list'),
    url(r'^tm/$', views.TMList.as_view(), name='material-list'),
    url(r'^responses/$', views.AnswersList.as_view(), name='answers-list'),
    url(r'^login/$', views.AuthView.as_view()),
    url(r'^add_news/$', views.NewsAdd.as_view(), name='news-add'),
    url(r'^add_tm/$', views.TMAdd.as_view(), name='material-add'),
    url(r'^answer/(?P<id>\d+)/$', views.AddAnswer.as_view(), name='add_answer'),
    url(r'^delete/m/(?P<id>\d+)/$', views.TMDelete.as_view(), name='material-delete'),
    url(r'^delete/n/(?P<id>\d+)/$', views.NewsDelete.as_view(), name='news-delete')
]
