from django.shortcuts import render
from django.views.generic import TemplateView
from .models import Route, Mail, Attachment
from braces.views import LoginRequiredMixin

# Create your views here.


class IndexView(LoginRequiredMixin,TemplateView):
    template_name = 'index.html'

    raise_exception = True
    def get_context_data(self, **kwargs):
        context = super(IndexView, self).get_context_data(**kwargs)

        mail = Route.objects.filter(fk_to=self.request.user)
        inbox = Mail.objects.get(id__in=mail)
        context['inbox']=inbox
        return context

