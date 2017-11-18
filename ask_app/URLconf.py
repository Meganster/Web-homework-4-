from django.conf.urls import patterns, url
from ask_app import views

urlpatterns = patterns('',
    url(r'^tag/(\d+)/$', views.tag),
    url(r'^question/(\d+)/$', views.question),
)
