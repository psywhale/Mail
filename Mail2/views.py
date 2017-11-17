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


        # Creating a context with the proper information.
        # Don't know of an easier way to do this.

        messages = Route.objects.filter(fk_to=self.request.user)
        email = []
        for message in messages:
            mail = {}
            m = message.fk_mail
            mail['id'] = m.id
            mail['subject'] = m.subject
            mail['read'] = message.read
            mail['termcode'] = m.termcode
            mail['section'] = m.section
            mail['from'] = m.fk_sender
            if Attachment.objects.filter(fk_mail=m):
                mail['has_attachment'] = True
            else:
                mail['has_attachment'] = False
            email.append(mail)
        context['email']=email
        return context

