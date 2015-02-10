# encoding=utf-8

"""
Special test module to try components which are currently under development.
These tests are not meant to be fully automated, it's rather a check that there
are no syntax errors in currently developed behavior and it behaves as expected
"""

from django.test import TestCase

from unittest import skipIf

from knowledge.models import Vertical, KnowledgeBuilder
from exercises.models import ExercisesCreator
from exercises.models import ExercisesGrader
from practice.models import Practicer
from smartoo.models import Session

# skip flag: whether to execute these special tests or not
SKIP = True

# test vertical
VERTICAL = '''
<doc id="7" url="http://en.wikipedia.org/wiki/Abraham_Lincoln"\
     title="Abraham Lincoln">
<p heading="1">
<term wuri="Abraham_Lincoln">
Abraham	NP	Abraham-n
Lincoln	NP	Lincoln-n
</term>
</p>
<p>
<s>
<term wuri="Abraham_Lincoln" uncertainty="1">
Abraham	NP	Abraham-n
Lincoln	NP	Lincoln-n
</term>
was	VBD	be-v
the	DT	the-x
<term wuri="List_of_Presidents_of_the_United_States">
16	CD	16-x
<g/>
th	NN	th-n
president	NN	president-n
of	IN	of-i
the	DT	the-x
United	NP	United-n
States	NPS	States-n
</term>
<g/>
.	SENT	.-x
</s>
<s>
Lincoln	NP	Lincoln-n
led	VVD	lead-v
the	DT	the-x
United	NP	United-n
States	NPS	States-n
through	IN	through-i
its	PP$	its-d
<term wuri="American_Civil_War">
Civil	NP	Civil-n
War	NP	War-n
</term>
<g/>
.	SENT	.-x
</s>
'''


class ComponentsTestCase(TestCase):
    def setUp(self):
        # create vertical, topic and session
        self.topic_uri = 'http://en.wikipedia.org/wiki/Abraham_Lincoln'
        Vertical.objects.create(
            topic_uri=self.topic_uri,
            content=VERTICAL)
        self.session = Session(topic_uri=self.topic_uri)
        # ------------------------------------------------------------------
        # components to test
        # ------------------------------------------------------------------
        self.session.knowledge_builder = KnowledgeBuilder.objects.create(
            behavior_name='simple',
            parameters={})
        self.session.exercises_creator = ExercisesCreator.objects.create(
            behavior_name='quasi',
            parameters={})
        self.session.exercises_grader = ExercisesGrader.objects.create(
            behavior_name='fake',
            parameters={})
        self.session.practicer = Practicer.objects.create(
            behavior_name='fake',
            parameters={})
        # ------------------------------------------------------------------
        # save session
        self.session.save()

    @skipIf(SKIP, "special components behavior test")
    def test_components(self):
        # there will whatever I want to test right now
        self.session.build_knowledge()
        self.session.create_graded_exercises()
        for exercise in self.session.get_graded_exercises():
            print exercise
