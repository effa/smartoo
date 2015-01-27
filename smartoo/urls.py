from django.conf.urls import patterns, include, url
from django.contrib import admin
from smartoo import views

urlpatterns = patterns('',
    # admin
    url(r'^admin/', include(admin.site.urls)),
    # gui views
    url(r'^$', views.home, name='home'),
    url(r'^practice/?P<topic>[^/]*)$', views.practice_session),
    # interface
    url(r'^interface/built-knowledge$', views.built_knowledge),
    url(r'^interface/create-exercises$', views.create_exercises),
    url(r'^interface/new-exercise$', views.new_exercise),
    url(r'^interface/session-feedback$', views.session_feedback)
)
