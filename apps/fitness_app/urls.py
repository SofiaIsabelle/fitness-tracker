from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.index),
    url(r'^register$', views.register),
    url(r'^login$', views.login),
    url(r'^dashboard$', views.dashboard),
    url(r'^logout$', views.logout),
    url(r'^new_workout$', views.new_workout),
    url(r'^add_workout$', views.add_workout),
    url(r'^follow/(?P<user_id>\d+)$', views.follow)
]