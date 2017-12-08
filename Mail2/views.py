from django.shortcuts import render, HttpResponse,redirect
from django.views.generic import TemplateView, FormView, View
from .models import Route, Mail, Attachment
from django.contrib.auth.models import User

from .forms import ReplyForm
from django.core.exceptions import PermissionDenied
from braces.views import LoginRequiredMixin, UserPassesTestMixin,GroupRequiredMixin
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
            if message.archived is False:
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


class ReplyView(LoginRequiredMixin, UserPassesTestMixin, FormView):

    template_name = 'reply.html'
    form_class = ReplyForm
    success_url = "/"
    raise_exception = True

    def test_func(self, user):
        route = Route.objects.get(fk_mail=Mail.objects.get(pk=self.kwargs['id']))
        return self.request.user == route.fk_to

    def get(self, request, *args, **kwargs):
        route = Route.objects.get(fk_mail=Mail.objects.get(pk=self.kwargs['id']))
        route.read = True
        route.save()
        return super(ReplyView, self).get(args, kwargs)

    def get_initial(self, **kwargs):
        initial = super(ReplyView, self).get_initial()
        if Mail.objects.filter(id=self.kwargs['id']).exists():
            mail_obj = Mail.objects.get(id=self.kwargs['id'])
            data = {}
            data['sendto'] = mail_obj.fk_sender_id
            data['termcode'] = mail_obj.termcode
            data['section'] = mail_obj.section
            data['subject'] = "RE: "+mail_obj.subject
            initial = data
        return initial
    
    def form_valid(self, form):
        new_msg = Mail()
        new_route = Route()
        new_msg.content = self.request.POST['content']
        new_msg.subject = self.request.POST['subject']
        new_msg.termcode = self.request.POST['termcode']
        new_msg.section = self.request.POST['section']
        new_msg.fk_sender = self.request.user
        new_msg.save()
        new_route.fk_to = User.objects.get(id=self.request.POST['sendto'])
        new_route.fk_mail = new_msg
        new_route.save()
        return super(ReplyView, self).form_valid(form)

        
        


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



class ArchiveMailView(LoginRequiredMixin, View):
    raise_exception = True
    #TODO make redirect to prev page not /

    def post(self, request):

        if Mail.objects.filter(id=request.POST['message_id']).exists():
            message = Mail.objects.get(id=request.POST['message_id'])
            if request.user.id == Route.objects.get(fk_mail=message).fk_to.id:
                message.archived = True
                message.save()
                return redirect("/")
            else:
                raise PermissionDenied
        else:
            raise PermissionDenied


class MarkMailUnreadView(LoginRequiredMixin, View):
    raise_exception = True
    #TODO make redirect to prev page not /

    def post(self, request):

        if Mail.objects.filter(id=request.POST['message_id']).exists():
            message = Mail.objects.get(id=request.POST['message_id'])
            route = Route.objects.get(fk_mail=message)
            pprint(route)
            if request.user.id == route.fk_to.id:
                route.read = False
                route.save()
                return redirect("/")
            else:
                raise PermissionDenied
        else:
            raise PermissionDenied



class AuditView(LoginRequiredMixin,GroupRequiredMixin,TemplateView):
    group_required = u"Auditors"
    template_name = 'audit.html'

    def get_context_data(self, **kwargs):
        context = super(AuditView, self).get_context_data(**kwargs)

        return context

    pass


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
        print(courses)
        results = {}
        for i, entry in enumerate(courses):
            # TODO Figure out why test fails but not real world.
            course = courses[entry]["course"]
            section, termcode = course.split("-")
            # print("section={},termcode={}".format(section,termcode));
            mails = Mail.objects.filter(termcode=termcode, section=section)
            unread_count = Route.objects.filter(fk_mail__in=mails, read=False, fk_to=request.user.id).count()

            results[i] = {"course": course, "count": unread_count }
        # print(results)
        return HttpResponse(json.dumps(results),content_type="application/json")
