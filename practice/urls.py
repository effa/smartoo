from django.conf.urls import patterns, url
from practice import views

urlpatterns = patterns('',
    url(r'^(?P<topic>[^/]*)$', views.start_practice),
    url(r'^interface/get-new-exercise$', views.get_new_exercise),
)
