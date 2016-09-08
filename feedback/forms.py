from django import forms


# TODO -- get rid of this * 
from .models import *

# TODO -- CONVERT THIS TO A MODEL FORM
class MissingSignFeedbackForm(forms.Form):
  
    handform = forms.ChoiceField(choices=handformChoices,  required=False,
        label='How many hands are used to make this sign?')
    handshape = forms.ChoiceField(choices=handshapeChoices, required=False,
        label='What is the handshape?')
    althandshape = forms.ChoiceField(choices=handshapeChoices, required=False, 
        label='What is the handshape of the left hand?')    
    location = forms.ChoiceField(choices=locationChoices, required=False,
        label='Choose the location of the sign on, or near the body')
    relativelocation = forms.ChoiceField(choices=relativelocationChoices, 
        label='Choose the location of the right hand on, or near the left hand', required=False)
    handbodycontact = forms.ChoiceField(choices=handbodycontactChoices, 
        label='Contact between hands and body', required=False)
    handinteraction = forms.ChoiceField(choices=handinteractionChoices, 
        label='Interaction between hands', required=False)
    direction = forms.ChoiceField(choices=directionChoices, 
        label='Movement direction of the hand(s)', required=False)
    movementtype = forms.ChoiceField(choices=movementtypeChoices, 
        label='Type of movement', required=False)
    smallmovement = forms.ChoiceField(choices=smallmovementChoices, 
        label='Small movements of the hand(s) and fingers', required=False)
    repetition = forms.ChoiceField(choices=repetitionChoices, 
        label='Number of movements', required=False)
    
    meaning = forms.CharField(label='Sign Meaning', 
        widget=forms.Textarea(attrs={'cols':'55', 'rows':'8'}))
    video = forms.FileField(required=False, 
        widget=forms.FileInput(attrs={'size':'60'}))
    comments = forms.CharField(label='Further Details', 
        widget=forms.Textarea(attrs={'cols':'55', 'rows':'8'}), required=False)
        
        
# TODO -- CONVERT THIS TO A MODEL FORM        
class SignFeedbackForm(forms.Form):
    """Form for input of sign feedback"""
  
    isAuslan = forms.ChoiceField(choices=isAuslanChoices, initial=0, widget=forms.RadioSelect)
    #isAuslan = forms.IntegerField(initial=0, widget=forms.HiddenInput)
    whereused = forms.ChoiceField(choices=whereusedChoices, initial="n/a")
    #whereused = forms.CharField(initial='n/a', widget=forms.HiddenInput)
    like = forms.ChoiceField(choices=likedChoices,  initial=0, widget=forms.RadioSelect)
    #like = forms.IntegerField(initial=0, widget=forms.HiddenInput)
    use = forms.ChoiceField(choices=useChoices, initial=0,  widget=forms.RadioSelect)
    #use = forms.IntegerField(initial=0, widget=forms.HiddenInput)
    suggested = forms.ChoiceField(choices=suggestedChoices, initial=3, required=False, widget=forms.RadioSelect)
    #suggested = forms.IntegerField(initial=0, widget=forms.HiddenInput)
    correct = forms.ChoiceField(choices=correctChoices, initial=0, widget=forms.RadioSelect)
    #correct = forms.IntegerField(initial=0, widget=forms.HiddenInput)
    kwnotbelong = forms.CharField(label="List keywords", required=False, widget=forms.Textarea) 
    comment = forms.CharField(required=False, widget=forms.Textarea)






