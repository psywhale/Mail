from django.shortcuts import render, HttpResponse
from django.views.generic import TemplateView, View
from .models import Route, Mail, Attachment

from braces.views import LoginRequiredMixin, UserPassesTestMixin
from django.db.models import Q
import simplejson as json
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator

from pprint import pprint

# Create your views here.


class IndexView(LoginRequiredMixin,TemplateView):
    template_name = 'index.html'
    raise_exception = True

    def get_context_data(self, **kwargs):
        context = super(IndexView, self).get_context_data(**kwargs)


        # Creating a context with the proper information.
        # Don't know of an easier way to do this.

        routes = Route.objects.filter(fk_to=self.request.user)

        email = []
        courses = []
        for route in routes:
            mail = {}
            message = route.fk_mail
            if message.section not in courses:
                courses.append(message.section)
            mail['id'] = message.id
            mail['subject'] = message.subject
            mail['read'] = route.read
            mail['termcode'] = message.termcode
            mail['section'] = message.section
            mail['date'] = str(message.created.month)+"/"+str(message.created.day)+"/"+str(message.created.year)
            mail['time'] = str(message.created.hour)+":"+str(message.created.minute)+":"+str(message.created.second)
            mail['timestamp'] = message.created.timestamp()
            #pprint(mail['date'])
            mail['from'] = message.fk_sender
            if Attachment.objects.filter(fk_mail=message):
                mail['has_attachment'] = True
            else:
                mail['has_attachment'] = False
            email.append(mail)
        context['email'] = email
        context['courses'] = courses
        return context

class ReplyView(LoginRequiredMixin, UserPassesTestMixin, TemplateView):

    template_name = 'reply.html'
    raise_exception = True

    def test_func(self, user):
        route = Route.objects.get(fk_mail=Mail.objects.get(pk=self.kwargs['id']))
        return self.request.user == route.fk_to

    def get(self, request, *args, **kwargs):
        route = Route.objects.get(fk_mail=Mail.objects.get(pk=self.kwargs['id']))
        route.read = True
        route.save()
        return super(ReplyView, self).get(args, kwargs)

    def get_context_data(self, **kwargs):
        context = super(ReplyView, self).get_context_data(**kwargs)
        if Mail.objects.filter(id=self.kwargs['id']).exists():
            m = Mail.objects.get(id=self.kwargs['id'])
            mail = m
            # mail['time'] = str(m.created.hour) + ":" + str(m.created.minute) + ":" + str(m.created.second)
            # mail['timestamp'] = m.created.timestamp()
            context['mail'] = mail
        else:
            print("oh noes")

        return context


class LabelView(LoginRequiredMixin, TemplateView):
    template_name = 'index.html'
    raise_exception = True

    def get_context_data(self, **kwargs):
        context = super(LabelView, self).get_context_data(**kwargs)

        # Creating a context with the proper information.
        # Don't know of an easier way to do this.

        termcoderaw = str(kwargs['sn']).split("-")
        termcode = termcoderaw[1].lower()
        section = termcoderaw[0].lower()


        routes = Route.objects.filter(fk_to=self.request.user)

        allmailincourse = Mail.objects.filter(termcode=termcode, section=section)
        allmailincourse_senttouser = allmailincourse.filter(route__fk_to=self.request.user)

        email = []
        courses = []
        if allmailincourse_senttouser.count() > 0:
            for message in allmailincourse_senttouser:
                mail = {}

                if message.section not in courses:
                    courses.append(message.section)
                mail['id'] = message.id
                mail['subject'] = message.subject
                mail['read'] = Route.objects.filter(fk_mail=message.id).get().read
                mail['termcode'] = message.termcode
                mail['section'] = message.section
                mail['date'] = str(message.created.month) + "/" + str(message.created.day) + "/" + str(message.created.year)
                mail['time'] = str(message.created.hour) + ":" + str(message.created.minute) + ":" + str(
                    message.created.second)
                mail['timestamp'] = message.created.timestamp()
                # pprint(mail['date'])
                mail['from'] = message.fk_sender
                if Attachment.objects.filter(fk_mail=message):
                    mail['has_attachment'] = True
                else:
                    mail['has_attachment'] = False
                email.append(mail)
            context['email'] = email
            context['courses'] = courses
        return context

class ListUnreadView(View):

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super(ListUnreadView, self).dispatch(request, *args, **kwargs)

    def post(self, request):



        courses = json.loads(request.body)


       # courses = self.request.POST['courses']
        results = []
        for course in courses['courses']:
            result = {}
            section, termcode = course.split("-")
            mails = Mail.objects.filter(termcode=termcode, section=section)
            #pprint(mails)
            unread_count = Route.objects.filter(fk_mail__in=mails, read=False, fk_to=self.request.user.id).count()
            result['course'] = course
            result['count'] = unread_count
            results.append(result)
        #print(json.dumps(results))
        return HttpResponse(json.dumps(results),content_type="application/json")
