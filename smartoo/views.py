from django.core.exceptions import ObjectDoesNotExist
from django.http import JsonResponse
#from django.http import HttpResponse
#from django.template import RequestContext, loader
from django.shortcuts import render

from common.utils.wiki import term_to_wiki_uri
from common.utils.http import BAD_REQUEST
from knowledge.utils.terms import name_to_term, term_to_name
#from knowledge.utils.topics import is_valid_topic
from smartoo.exceptions import SessionError
from smartoo.models import Session
import json


# ----------------------------------------------------------------------------
#  Views
# ----------------------------------------------------------------------------

def home(request):
    return render(request, 'smartoo/home.html')


def practice_session(request, topic_name):
    """
    Main view for practice session.
    Returns base HTML page for the practice session.
    """
    return render(request, 'smartoo/practice.html', {
        'topic': term_to_name(topic_name),
        'topicURI': term_to_wiki_uri(topic_name)})


# ----------------------------------------------------------------------------
#  Interface (controllers)
# ----------------------------------------------------------------------------

#def start_session(request, topic_name):
def start_session(request):
    """
    Creates new session for given topic, selects components.
    """
    #topic_name = request.POST.get("topic")
    #print request.POST
    #print 'topic_name =', topic_name

    post_data = json.loads(request.body)
    topic_name = post_data.get('topic')

    if not topic_name:
        return JsonResponse({"success": False, "message": "Request without topic."},
            status=BAD_REQUEST)

    # TODO: normalizace tematu, osetretni neexistence termatu!!!, ...
    # ale to by melo nastat uz ve view practice_session
    try:
        topic = name_to_term(topic_name)
    except ValueError:
        return JsonResponse({"success": False, "message": "Invalid topic."},
            status=BAD_REQUEST)

    try:
        # create session and select components
        session = Session.objects.create_with_components(topic=topic)
        # remember the session id
        request.session['session_id'] = session.id
        return JsonResponse({"success": True})
    except ValueError:
        # TODO: specialni zpracovani napr. DisambiguationError
        # topic doesn't exist, don't create a session
        return JsonResponse({"success": False, "message": "No such topic."},
            status=BAD_REQUEST)


# NOTE: all views are in the main smartoo app, since they use Session model

def build_knowledge(request):
    """
    Builds knowledge (if not already built) and returns "done" message.
    """
    try:
        session = retrieve_current_session(request)
        session.build_knowledge()
        return JsonResponse({"success": True})
    except SessionError:
        return JsonResponse({"success": False}, status=BAD_REQUEST)


def create_exercises(request):
    """
    Creates exercises (if not already created) and returns "done" message.
    """
    try:
        session = retrieve_current_session(request)
        session.create_graded_exercises()
        return JsonResponse({"success": True})
    except SessionError:
        return JsonResponse({"success": False}, status=BAD_REQUEST)


def next_exercise(request):
    """
    Saves the feedback from previous exercise and returns a new exercise
    (or feedback form, if the session is over).
    """
    try:
        session = retrieve_current_session(request)

        # if there is feedback for the previous exercise, process it
        if request.body:
            post_data = json.loads(request.body)
            feedback = post_data.get('feedback')
            if feedback:
                session.provide_feedback(feedback)

        exercise = session.next_exercise()
        if exercise is None:
            # show feedback form
            return JsonResponse({'success': True, 'finnished': True})

        exercise_dict = exercise.data
        exercise_dict['pk'] = exercise.pk

        response_data = {
            'success': True,
            'finnished': False,
            'exercise': exercise_dict
        }

        return JsonResponse(response_data)
    except SessionError:
        return JsonResponse({"success": False}, status=BAD_REQUEST)


def session_feedback(request):
    """
    Saves global feedback for the whole session.
    """
    try:
        session = retrieve_current_session(request)

        post_data = json.loads(request.body)
        rating = post_data.get('rating')
        session.provide_final_feedback(rating)

        return JsonResponse({'success': True})
    except SessionError:
        return JsonResponse({"success": False}, status=BAD_REQUEST)


# ----------------------------------------------------------------------------
#  Helper functions
# ----------------------------------------------------------------------------

#def render_exercise(request, exercise):
#    """Renders exercise according to exercise type (multichoice etc.)
#    """
#    return render(request, 'practice/multichoice-question.html', exercise)


def retrieve_current_session(request):
    """
    Returns session for current request.

    Raises:
        SessionError: if there is not current session
    """
    try:
        session_id = request.session['session_id']
        session = Session.objects.get(id=session_id)
        return session
    except KeyError:
        raise SessionError("No session_id stored in the session.")
    except ObjectDoesNotExist:
        raise SessionError("Session with id=%s doesn't exist." % session_id)
