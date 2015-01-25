#from django.http import JsonResponse
#from django.template import RequestContext, loader
from django.shortcuts import render
from practice.models import SessionManager
#import json


# ----------------------------------------------------------------------------
#  Views
# ----------------------------------------------------------------------------

def start_practice(request, topic):
    request.session['topic'] = topic
    #template = loader.get_template('smartoosession/index.html')
    #context = RequestContext(request, topic)
    #return HttpResponse(template.render(context))
    print 'start practice'
    request.session['manager'] = SessionManager(topic)
    print 'key', request.session.session_key
    return render(request, 'practice/index.html', {
        'topic': topic})


# ----------------------------------------------------------------------------
#  Interface (for AJAX)
# ----------------------------------------------------------------------------

def get_new_exercise(request):
    """Returns HTML response with new exercise rendered
    """
    print 'key', request.session.session_key
    try:
        session_manager = request.session['manager']
        exercise = session_manager.get_new_exercise()
        # vysledek je potreba znova ulozit do cache ?!
        request.session['manager'] = session_manager
        #return JsonResponse(exercise)
        return render_exercise(request, exercise)
    except:
        # TODO: asi nejakou chybovou informaci?
        raise


# ----------------------------------------------------------------------------
#  Helper functions
# ----------------------------------------------------------------------------

def render_exercise(request, exercise):
    """Renders exercise according to exercise type (multichoice etc.)
    """
    return render(request, 'practice/multichoice-question.html', exercise)
