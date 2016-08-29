from django.shortcuts import render, get_object_or_404, redirect
from django.conf import settings 
from django.views.generic.edit import CreateView, FormView
from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy, reverse 
from django.http import HttpResponseRedirect
from django.contrib import messages

from .models import GeneralFeedback, MissingSignFeedback, SignFeedback
from .forms import MissingSignFeedbackForm, SignFeedbackForm


def index(request):
    return render(request, "feedback/index.html",
        {"language": settings.LANGUAGE_NAME,               
         "country": settings.COUNTRY_NAME,})
                    
                    
class GeneralFeedbackCreate(SuccessMessageMixin, CreateView):
    '''
    This class implements the general feedback form
    '''
    model = GeneralFeedback
    fields = ["comment", "video"]
    success_url = reverse_lazy("feedback:generalfeedback")
    success_message = "Thanks for your comment. We value your contribution."
    
    
# TODO -- Make this function better -- possibly by using CreateView      
def missingsign(request):
    posted = False # was the feedback posted?
    
    if request.method == "POST":
        
        fb = MissingSignFeedback()

        form = MissingSignFeedbackForm(request.POST, request.FILES)
        
        if form.is_valid(): 
            
            # either we get video of the new sign or we get the 
            # description via the form
            
            if 'video' in form.cleaned_data and form.cleaned_data['video'] != None:
                fb.video = form.cleaned_data['video']

            else:
                # get sign details from the form 
                fb.handform = form.cleaned_data['handform'] 
                fb.handshape = form.cleaned_data['handshape']
                fb.althandshape = form.cleaned_data['althandshape']
                fb.location = form.cleaned_data['location']
                fb.relativelocation = form.cleaned_data['relativelocation']
                fb.handbodycontact = form.cleaned_data['handbodycontact']
                fb.handinteraction = form.cleaned_data['handinteraction']
                fb.direction = form.cleaned_data['direction']
                fb.movementtype = form.cleaned_data['movementtype']
                fb.smallmovement = form.cleaned_data['smallmovement']
                fb.repetition = form.cleaned_data['repetition']
            
            # these last two are required either way (video or not)
            fb.meaning = form.cleaned_data['meaning']
            fb.comments = form.cleaned_data['comments']
    
            fb.save()
            posted = True
            messages.success(request, "Thanks for your comment. We value your contribution.") 
            return HttpResponseRedirect(reverse('feedback:missingsign'))               
    else:
        form = MissingSignFeedbackForm()

    return render(request, 'feedback/missingsign_form.html',
                               {
                                'language': settings.LANGUAGE_NAME,
                                'country': settings.COUNTRY_NAME,
                                'title':"Report a Missing Sign",
                                'posted': posted,
                                'form': form
                                })
                            

def signfeedback(request, keyword, n):
    # POST request -- save the submitted feedback if it's valid
    if request.method == "POST":
        form = SignFeedbackForm(request.POST)
        if form.is_valid():                                   
            clean = form.cleaned_data
            # create a SignFeedback object to store the result in the db
            saved_feedback = SignFeedback(
                isAuslan=clean['isAuslan'],
                whereused=clean['whereused'],
                like=clean['like'],
                use=clean['use'],
                suggested=clean['suggested'],
                correct=clean['correct'],
                kwnotbelong=clean['kwnotbelong'],
                comment=clean['comment'],
                #user=request.user,
                word = '%s-%s'%(keyword, n)
                )
            saved_feedback.save()
            
            messages.success(request, "Thanks for your comment. We value your contribution.")
            return HttpResponseRedirect(reverse('feedback:signfeedback', 
                kwargs={'keyword': keyword, 'n': n}))
                           
   # Any other kind of request -- create the empty feedback form        
    else:
        form = SignFeedbackForm()
   
    # Serve the empty feedback form to the user     
    return render(request, "feedback/signfeedback_form.html", {"form": form})


def showfeedback(request):
    """
    View to list the feedback that's been left on the site.
    """    
    general = GeneralFeedback.objects.filter(status='unread')
    missing = MissingSignFeedback.objects.filter(status='unread')
    signfb = SignFeedback.objects.filter(status__in=('unread', 'read'))
    return render(request, "feedback/show.html",
        {'general': general,
         'missing': missing,
         'signfb': signfb,
        })
        
        
def delete(request, kind, id):
    """
    Mark a feedback item as deleted, kind 'signfeedback', 
    'generalfeedback' or 'missingsign'.
    """
    if kind == 'sign':
        kind = SignFeedback
    elif kind == 'general':
        kind = GeneralFeedback
    elif kind == 'missingsign':
        kind = MissingSignFeedback
    else:
        raise Http404    
    item = get_object_or_404(kind, id=id)
    # mark as deleted
    item.status = 'deleted'
    item.save()
    # return to referer
    if 'HTTP_REFERER' in request.META:
        url = request.META['HTTP_REFERER']
    else:
        url = '/'
    return redirect(url)
                          
                    
