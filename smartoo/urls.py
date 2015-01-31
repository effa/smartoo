from django.conf.urls import patterns, include, url
from django.contrib import admin
from smartoo import views

urlpatterns = patterns('',
    # admin
    url(r'^admin/', include(admin.site.urls)),
    # gui views
    url(r'^$', views.home, name='home'),
    url(r'^practice/(?P<topic>[^/]*)$', views.practice_session),
    # interface
    url(r'^interface/start-session/(?P<topic>[^/]*)$', views.start_session),
    url(r'^interface/knowledge/', include('knowledge.urls')),
    url(r'^interface/exercises/', include('exercises.urls')),
    url(r'^interface/new-exercise$', views.new_exercise),
    url(r'^interface/session-feedback$', views.session_feedback)
)
