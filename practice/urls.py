from django.conf.urls import patterns, url
from practice import views

urlpatterns = patterns('',
    url(r'^(?P<topic>[^/]*)$', views.practice_session),
    url(r'^interface/built-knowledge$', views.built_knowledge),
    url(r'^interface/create-exercises$', views.create_exercises),
    url(r'^interface/new-exercise$', views.new_exercise),
    url(r'^interface/session-feedback$', views.session_feedback)
)
