from django.shortcuts import render
from django.views.generic import TemplateView
from .models import Route, Mail, Attachment
from braces.views import LoginRequiredMixin

# Create your views here.


class IndexView(LoginRequiredMixin,TemplateView):
    template_name = 'index.html'
