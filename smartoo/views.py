from django.core.exceptions import ObjectDoesNotExist
from django.http import JsonResponse
#from django.http import HttpResponse
#from django.template import RequestContext, loader
from django.shortcuts import render
#from common.utils.wiki import name_to_resource_uri
from knowledge.utils.terms import name_to_term, term_to_name
from knowledge.utils.topics import is_valid_topic
from smartoo.exceptions import SessionError
from smartoo.models import Session
#import json


# ----------------------------------------------------------------------------
#  Views
# ----------------------------------------------------------------------------

def home(request):
    # TODO: home template
    pass


def practice_session(request, topic_name):
    """
    Main view for practice session.
    Returns base HTML page for the practice session.
    """
    return render(request, 'smartoo/index.html', {
        'topic': term_to_name(topic_name)})


# ----------------------------------------------------------------------------
#  Interface
# ----------------------------------------------------------------------------

def start_session(request, topic_name):
    """
    Creates new session for given topic, selects components.
    """
    # TODO: normalizace tematu, osetretni neexistence termatu!!!, ...
    # ale to by melo nastat uz ve view practice_session
    topic = name_to_term(topic_name)
    if is_valid_topic(topic):
        # create session and select components
        # TODO: i nasledujici operace muze selhat, osetrit...
        session = Session.objects.create_with_components(topic=topic)
        # remember the session id
        request.session['session_id'] = session.id
        return JsonResponse({"success": True})
    else:
        # topic doesn't exist, don't create a session
        # TODO: ? suggest "near" topics? ("Did you mean ... ?")
        return JsonResponse({"success": False})


# NOTE: all views are in the main smartoo app, since they use Session model

def build_knowledge(request):
    """
    Builds knowledge (if not already built) and returns "done" message.
    """
    try:
        session = retrieve_current_session(request)
        session.build_knowledge()
        return JsonResponse({"success": True})
    except (AttributeError, SessionError):
        return JsonResponse({"success": False})


def create_exercises(request):
    """
    Creates exercises (if not already created) and returns "done" message.
    """
    session = retrieve_current_session(request)
    session.create_graded_exercises()
    return JsonResponse({"success": True})


def new_exercise(request):
    """
    Saves the feedback from previous exercise and returns a new exercise
    (or feedback form, if the session is over).
    """
    #print 'key', request.session.session_key
    try:
        session = retrieve_current_session(request)
        # retrieve current session
        #session_id = request.session['session_id']
        #session = Session.objects.get(id=session_id)

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


def retrieve_current_session(request):
    """
    Returns session for current request. (None if there is no current session.)
    """
    try:
        session_id = request.session['session_id']
        session = Session.objects.get(id=session_id)
        return session
    except (KeyError, ObjectDoesNotExist):
        return None
