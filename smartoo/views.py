#from django.http import JsonResponse
from django.http import HttpResponse
#from django.template import RequestContext, loader
from django.shortcuts import render
from common.utils.wiki import name_to_uri
from knowledge.models import Topic
from smartoo.models import Session
#import json


# ----------------------------------------------------------------------------
#  Views
# ----------------------------------------------------------------------------

def home(request):
    # TODO: home template
    pass


def practice_session(request, topic):
    """
    Main view for practice session.
    Returns base HTML page for the practice session.
    """
    return render(request, 'smartoo/index.html', {
        'topic': topic.get_name()})


# ----------------------------------------------------------------------------
#  Interface
# ----------------------------------------------------------------------------

def start_session(request, topic):
    """
    Creates new session for given topic, selects components.
    """
    # TODO: vytvoreni tematu ... musi existovat v DB vsech temat
    # TODO: normalizace tematu, osetretni neexistence, ...
    topic = Topic.objects.get(uri=name_to_uri(topic))

    # create session and select components
    session = Session(topic=topic)
    session.select_components()
    session.save()

    # remember the session id
    request.session['session_id'] = session.id
    # print 'key', request.session.session_key

    # Vysledek asi predavat nejak inteligentneji??
    return HttpResponse("done")


def new_exercise(request):
    """
    Saves the feedback from previous exercise and returns a new exercise
    (or feedback form, if the session is over).
    """
    #print 'key', request.session.session_key
    try:
        # retrieve current session
        session_id = request.session['session_id']
        session = Session.objects.get(id=session_id)

        # get a new exercise, render it and return
        exercise = session.get_new_exercise()
        # TODO: pokud uz je konec session, vratit feedback form
        #return JsonResponse(exercise)
        return render_exercise(request, exercise)

    except:
        # TODO: asi nejakou chybovou informaci?
        raise


def session_feedback(request):
    """
    Saves global feedback for the whole session.
    """
    pass


# ----------------------------------------------------------------------------
#  Helper functions
# ----------------------------------------------------------------------------

def render_exercise(request, exercise):
    """Renders exercise according to exercise type (multichoice etc.)
    """
    return render(request, 'practice/multichoice-question.html', exercise)
