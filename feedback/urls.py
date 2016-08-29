from django.conf.urls import url

from . import views

app_name = "feedback"
urlpatterns = [  
    # ex: /
    url(r"^$", views.index, name="index"),
    # ex: generalfeedback/
    url(r"^generalfeedback/$", views.GeneralFeedbackCreate.as_view(), 
        name="generalfeedback"),
    # ex: show/
    url(r'^show', views.showfeedback, name = 'showfeedback'),
    # ex: general/delete/1/
    url(r'^(?P<kind>general|sign|missingsign)/delete/(?P<id>\d+)/$', 
    views.delete, name = 'delete'),
    # ex: missingsign/
    url(r'^missingsign/$', views.missingsign,
        name='missingsign'),
    # ex: abscond-1/     
    url(r'^sign/(?P<keyword>.+)-(?P<n>\d+)/$', views.signfeedback,
        name = 'signfeedback'),         
]   



