from django.conf.urls import patterns, include, url
from django.contrib import admin
from smartoo import views

urlpatterns = patterns('',
    # admin
    url(r'^admin/', include(admin.site.urls)),
    # gui views
    url(r'^$', views.home, name='home'),
    url(r'^practice/(?P<topic_name>[^/]*)$', views.practice_session),
    # interface
    url(r'^interface/start-session$', views.start_session),
    url('^interface/build-knowledge$', views.build_knowledge),
    url('^interface/create-exercises$', views.create_exercises),
    url(r'^interface/next-exercise$', views.next_exercise),
    url(r'^interface/session-feedback$', views.session_feedback)
)
