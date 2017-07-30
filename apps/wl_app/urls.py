
from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.index),
    url(r'^main$', views.index),
    url(r'^login$', views.login),
    url(r'^register$', views.register),
    url(r'^my_page$', views.my_page),
    url(r'^add$', views.add),
    url(r'^wish_item/(?P<wish_id>\d+)', views.wish_item),
    url(r'^create$', views.create),
    url(r'^home$', views.home),
    url(r'^logout$', views.logout),
    url(r'^delete/(?P<wish_id>\d+)$', views.delete),
    url(r'^remove/(?P<wish_id>\d+)$', views.remove),
    url(r'^join/(?P<wish_id>\d+)', views.join),
]
