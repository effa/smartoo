from django.conf.urls import patterns, url
from exercises import views


urlpatterns = patterns('',
        url('^create-exercises$', views.create_exercises)
)
