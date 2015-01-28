from django.conf.urls import patterns, url
from knowledge import views


urlpatterns = patterns('',
        url('^build-knowledge$', views.build_knowledge)
)
