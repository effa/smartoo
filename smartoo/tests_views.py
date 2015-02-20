# encoding=utf-8

from __future__ import unicode_literals
#from django.core.urlresolvers import reverse
from django.test import TestCase
from knowledge.namespaces import TERM
from smartoo.models import Session
from json import loads


class StartSessionViewTestCase(TestCase):
    fixtures = ['fake-components-vertical.xml']

    def setUp(self):
        pass

    def test_start_session_successfully(self):
        response = self.client.post('/interface/start-session/Abraham_Lincoln')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(loads(response.content)["success"], True)
        sessions = Session.objects.all()
        self.assertEqual(len(sessions), 1)
        session = sessions[0]
        self.assertEqual(session.topic, TERM['Abraham_Lincoln'])

    def test_start_session_unsuccessfully(self):
        response = self.client.post('/interface/start-session/Some_nonsense')
        #self.assertEqual(response.status_code, 200)
        #print 'code', response.status_code
        self.assertEqual(loads(response.content)["success"], False)
        sessions = Session.objects.all()
        self.assertEqual(len(sessions), 0)

# TODO: tests for all views

#class BuildKnowledgeViewTests(TestCase):
#    fixtures = ['fake-components-vertical.xml']

#    def setUp(self):
#        # set up a session with fake components
#        session = Session(topic=TER)
#        session.select_components()
#        session.save()

#        # remember the session id
#        request.session['session_id'] = session.id

#        self.client.session[

#    def buid_knowledge_test(self):
#        response = self.client.post(reverse('build-knowledge'))
#        self.assertEqual(response.status_code, 200)
