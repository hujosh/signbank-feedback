# -*- coding: utf-8 -*-
from django.views.generic import (
    CreateView,
    DeleteView,
    DetailView,
    UpdateView,
    ListView
)

from .models import (
	SignFeedback,
	MissingSignFeedback,
	GeneralFeedback,
)


class SignFeedbackCreateView(CreateView):

    model = SignFeedback


class SignFeedbackDeleteView(DeleteView):

    model = SignFeedback


class SignFeedbackDetailView(DetailView):

    model = SignFeedback


class SignFeedbackUpdateView(UpdateView):

    model = SignFeedback


class SignFeedbackListView(ListView):

    model = SignFeedback


class MissingSignFeedbackCreateView(CreateView):

    model = MissingSignFeedback


class MissingSignFeedbackDeleteView(DeleteView):

    model = MissingSignFeedback


class MissingSignFeedbackDetailView(DetailView):

    model = MissingSignFeedback


class MissingSignFeedbackUpdateView(UpdateView):

    model = MissingSignFeedback


class MissingSignFeedbackListView(ListView):

    model = MissingSignFeedback


class GeneralFeedbackCreateView(CreateView):

    model = GeneralFeedback


class GeneralFeedbackDeleteView(DeleteView):

    model = GeneralFeedback


class GeneralFeedbackDetailView(DetailView):

    model = GeneralFeedback


class GeneralFeedbackUpdateView(UpdateView):

    model = GeneralFeedback


class GeneralFeedbackListView(ListView):

    model = GeneralFeedback

