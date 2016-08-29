from django.conf.urls import include, url


urlpatterns = [
    url(r"^", include("feedback.urls", namespace="feedback")),
]
