from django.shortcuts import render, get_object_or_404, redirect
from django.conf import settings 
from django.views.generic.edit import CreateView, FormView
from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy, reverse 
from django.http import HttpResponseRedirect, HttpResponseNotFound
from django.contrib import messages
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth.mixins import LoginRequiredMixin

from feedback.models import GeneralFeedback, MissingSignFeedback, SignFeedback
from feedback.forms import MissingSignFeedbackForm, SignFeedbackForm


def index(request):
    return render(request, "feedback/index.html",
        {"language": settings.LANGUAGE_NAME,               
        "country": settings.COUNTRY_NAME,})
                    
                    
class GeneralFeedbackCreate(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    '''
    This class implements the general feedback form.
    '''
    model = GeneralFeedback
    fields = ["comment", "video"]
    success_url = reverse_lazy("feedback:generalfeedback")
    success_message = "Thanks for your comment. We value your contribution."
    
    def form_valid(self, form):
        form.instance.user = self.request.user
        return super(GeneralFeedbackCreate, self).form_valid(form)


@login_required      
def missingsign(request):
    if request.method == "POST":
        form = MissingSignFeedbackForm(request.POST, request.FILES)
        if form.is_valid():
            form_to_save = form.save(commit=False)
            form_to_save.user = request.user
            form_to_save.save()
            success_message = 'Thank you for your feedback. Note that addressing your feedback may take some time depending on the level of requests.'
            messages.success(request, success_message) 
            return HttpResponseRedirect(reverse('feedback:missingsign'))  
    # Any other kind of request goes here     
    else:
        form = MissingSignFeedbackForm()
    return render(request, 'feedback/missingsign_form.html',
                               {
                                'language': settings.LANGUAGE_NAME,
                                'country': settings.COUNTRY_NAME,
                                'title':"Report a Missing Sign",
                                'form': form
                                })      
                                            
@login_required                                                    
def wordfeedback(request, keyword, n):
    if request.method == "POST":
        form = SignFeedbackForm(request.POST)
        if form.is_valid():
            # This is the name of the sign.
            name = '%s-%s'%(keyword, n)                                   
            save_signfeedback(request, form, name)
            messages.success(request, 'Thank you for your comment. We value your contribution') 
            return HttpResponseRedirect(reverse('feedback:wordfeedback', 
                kwargs={'keyword': keyword, 'n': n}))                    
   # Any other kind of request goes here
    else:
        form = SignFeedbackForm()
    return render(request, "feedback/signfeedback_form.html", {"form": form})

@login_required    
def glossfeedback(request, gloss_number):
    if request.method == "POST":
        form = SignFeedbackForm(request.POST)
        if form.is_valid():
            # This is the name of the gloss.
            name = '%s'%(gloss_number)                           
            save_signfeedback(request, form, name)
            messages.success(request, 'Thank you for your comment. We value your contribution') 
            return HttpResponseRedirect(reverse('feedback:glossfeedback', 
                kwargs={'gloss_number': gloss_number}))                    
   # Any other kind of request goes here
    else:
        form = SignFeedbackForm()
    return render(request, "feedback/signfeedback_form.html", {"form": form})
    
    
def save_signfeedback(request, form, name):
    '''
    Do the work of saving feedback for a sign or gloss.
    '''                           
    form_to_save = form.save(commit=False)
    form_to_save.user= request.user
    form_to_save.name = name
    form_to_save.save()

@permission_required('feedback.delete_generalfeedback')
def showfeedback(request):
    '''
    View to list the feedback that's been left on the site.
    '''
    general = GeneralFeedback.objects.filter(status='unread')
    missing = MissingSignFeedback.objects.filter(status='unread')
    signfb = SignFeedback.objects.filter(status__in=('unread', 'read'))
    return render(request, "feedback/show.html",
        {'general': general,
         'missing': missing,
         'signfb': signfb
        }
    )
        

        
@permission_required('feedback.delete_generalfeedback')
def delete(request, kind, id):
    '''
    Mark a feedback item as deleted. 
    kind can be either 'sign', 'general' or 'missingsign'.
    '''
    if kind == 'sign':
        kind = SignFeedback
    elif kind == 'general':
        kind = GeneralFeedback
    elif kind == 'missingsign':
        kind = MissingSignFeedback
    else:
        # Django treats this as a 500 error, and 
        # tries to load 500.html stored in the root 
        # template directory of the website. 
        raise ValueError()
    feedback_to_delete = get_object_or_404(kind, pk=id)
    # mark as deleted
    feedback_to_delete.status = 'deleted'
    feedback_to_delete.save()
    # return to referer
    if 'HTTP_REFERER' in request.META:
        url = request.META['HTTP_REFERER']
    else:
        url = '/'
    return redirect(url)
                          
                    
