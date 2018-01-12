from django.shortcuts import render, HttpResponse,redirect
from django.views.generic import TemplateView, FormView, View
from .models import Route, Mail, Attachment
from django.contrib.auth.models import User
from Mail2proj.settings import DEBUG
from .forms import ReplyForm, ComposeForm, AuditClassForm, AuditUserForm
from django.core.exceptions import PermissionDenied
from braces.views import LoginRequiredMixin, UserPassesTestMixin,GroupRequiredMixin
from django.db.models import Q
import simplejson as json, re
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from LTI.lti import LtiLaunch
from pprint import pprint
from django.contrib.auth import login
# Create your views here.


class IndexView(LoginRequiredMixin,TemplateView):
    template_name = 'index.html'
    raise_exception = True

    def get_context_data(self, **kwargs):
        context = super(IndexView, self).get_context_data(**kwargs)


        # Creating a context with the proper information.
        # Don't know of an easier way to do this.

        routes = Route.objects.filter(to=self.request.user.username)

        email = []
        courses = []
        for route in routes:
            mail = {}
            message = route.fk_mail
            # if message.section not in courses:
            #     courses.append(message.section)
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
        context['session'] = self.request.session
        # context['courses'] = courses
        return context


class OutboxView(LoginRequiredMixin,TemplateView):
    template_name = 'outbox.html'
    raise_exception = True

    def get_context_data(self, **kwargs):
        context = super(OutboxView, self).get_context_data(**kwargs)


        # Creating a context with the proper information.
        # Don't know of an easier way to do this.

        usermails = Mail.objects.filter(fk_sender=self.request.user)


        email = []
        courses = []
        for usermail in usermails:
            mail = {}

            route = Route.objects.get(fk_mail=usermail)
            # if message.section not in courses:
            #     courses.append(message.section)
            #if usermail.fk_sender is self.request.user:
            tofields = User.objects.get(username=route.to).get_full_name()

            mail['id'] = usermail.id
            mail['subject'] = usermail.subject
            mail['read'] = route.read
            mail['to'] = tofields
            mail['termcode'] = usermail.termcode
            mail['section'] = usermail.section
            mail['date'] = str(usermail.created.month)+"/"+str(usermail.created.day)+"/"+str(usermail.created.year)
            mail['time'] = str(usermail.created.hour)+":"+str(usermail.created.minute)+":"+str(usermail.created.second)
            mail['timestamp'] = usermail.created.timestamp()
            #pprint(mail['date'])
            mail['from'] = usermail.fk_sender
            if Attachment.objects.filter(fk_mail=usermail):
                mail['has_attachment'] = True
            else:
                mail['has_attachment'] = False
            email.append(mail)
        context['email'] = email
        context['session'] = self.request.session
        #dprint(email)
        # context['courses'] = courses
        return context


class ComposeView(LoginRequiredMixin, FormView):
    template_name = 'compose.html'
    form_class = ComposeForm
    success_url = "/"
    raise_exception = True

    def form_valid(self, form):
        new_msg = Mail()
        new_route = Route()
        new_msg.content = self.request.POST['content']
        new_msg.subject = self.request.POST['subject']
        new_msg.termcode = self.request.POST['termcode']
        new_msg.section = self.request.POST['section']
        new_msg.fk_sender = self.request.user
        new_msg.save()
        new_route.to = self.request.POST['sendto']
        new_route.fk_mail = new_msg
        new_route.save()
        return super(ComposeView, self).form_valid(form)

    def get_context_data(self, **kwargs):

        context = super(ComposeView, self).get_context_data(**kwargs)
        if 'sn' in self.kwargs:
            context['sn'] = self.kwargs['sn']
        else:
            context['sn'] = 'False'
        context['session'] = self.request.session
        return context


class ReplyView(LoginRequiredMixin, UserPassesTestMixin, FormView):

    template_name = 'reply.html'
    form_class = ReplyForm
    success_url = "/"
    raise_exception = True

    def test_func(self, user):
        route = Route.objects.get(fk_mail=Mail.objects.get(pk=self.kwargs['id']))
        return self.request.user.username == route.to

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
            username = User.objects.get(id=mail_obj.fk_sender_id).username
            data['sendto'] = username
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
        new_route.to =self.request.POST['sendto']
        new_route.fk_mail = new_msg
        new_route.save()
        return super(ReplyView, self).form_valid(form)

    def get_context_data(self, **kwargs):
        #
        # content = models.TextField()
        # subject = models.CharField(max_length=512)
        # termcode = models.CharField(max_length=4)
        # section = models.CharField(max_length=5)
        # archived = models.BooleanField(default=False)
        # fk_sender = models.ForeignKey(User)
        # created = models.DateTi
        context = super(ReplyView, self).get_context_data(**kwargs)
        info = {}

        if Mail.objects.filter(id=self.kwargs['id']).exists():
            m = Mail.objects.get(id=self.kwargs['id'])
            r = Route.objects.get(fk_mail=m)
            info= {
                'id': m.id,
                'content': m.content,
                'subject': m.subject,
                'termcode': m.termcode,
                'section': m.section,
                'fk_sender': m.fk_sender,
                'to': r.to,
                'created': m.created,
            }

            context['mail'] = info
            # dprint(context)
        else:
            # todo raise error
            print("oh noes")
        context['session'] = self.request.session
        return context


class OutboxReplyView(ReplyView):

    def test_func(self, user):
        mail = Mail.objects.get(pk=self.kwargs['id'])
        return self.request.user == mail.fk_sender

    def get_initial(self, **kwargs):
        initial = super(OutboxReplyView, self).get_initial()
        if Mail.objects.filter(id=self.kwargs['id']).exists():
            mail_obj = Mail.objects.get(id=self.kwargs['id'])
            router = Route.objects.get(fk_mail=mail_obj)
            data = {}
            data['sendto'] = router.to
            data['termcode'] = mail_obj.termcode
            data['section'] = mail_obj.section
            data['subject'] = "RE: "+mail_obj.subject
            initial = data
        return initial



class ArchiveMailView(LoginRequiredMixin, View):
    raise_exception = True
    #TODO make redirect to prev page not /

    def post(self, request):

        if Mail.objects.filter(id=request.POST['message_id']).exists():
            message = Mail.objects.get(id=request.POST['message_id'])
            if request.user.username == Route.objects.get(fk_mail=message).to:
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
            if request.user.username == route.to:
                route.read = False
                route.save()
                message.archived = False
                message.save()
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
        context['session'] = self.request.session
        return context


class AuditViewClass(AuditView, FormView):
    form_class = AuditClassForm

    def get_initial(self, **kwargs):
        initial = super(AuditViewClass, self).get_initial()
        data = []
        dataqs = Mail.objects.values('section','termcode').annotate().distinct()
        for row in dataqs:
            data.append(row["section"] + "-" + row["termcode"])
        dprint(data)
        initial["audit_class"] = data
        dprint(initial)
        return data


class AuditViewUser(AuditView, FormView):
    form_class = AuditUserForm

    def get_initial(self, **kwargs):
        data = super(AuditViewUser, self).get_initial()
        return data



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


        routes = Route.objects.filter(to=self.request.user.username)

        allmailincourse = Mail.objects.filter(termcode=termcode, section=section)
        allmailincourse_senttouser = allmailincourse.filter(route__to=self.request.user.username)

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
        context['session'] = self.request.session
        return context

class ListUnreadView(View):

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super(ListUnreadView, self).dispatch(request, *args, **kwargs)

    def post(self, request):
        courses = json.loads(request.body)
        # dprint(courses)
        results = {}

        for i, entry in enumerate(courses):
            # TODO Figure out why test fails but not real world.
            course =courses[entry]['course']
            section, termcode = course.split("-")
            # print("section={},termcode={}".format(section,termcode));
            mails = Mail.objects.filter(termcode=termcode, section=section)
            unread_count = Route.objects.filter(fk_mail__in=mails, read=False, to=request.user.username).count()
            results[i] = {"course": course, "count": unread_count }
        return HttpResponse(json.dumps(results),content_type="application/json")

class Launch(LtiLaunch):

    def post(self, request, *args, **kwargs):

        # flushing the session prevents conflicting sessions when the open multiple tabs/windows.
        self.request.session.flush()
        # Returns tp if valid LTI user
        tp = self.is_lti_valid(request)
        if tp is not None:
            # Get the user or add them if they do not currently exist
            user = self.get_or_add_user(tp)
            params = tp.to_params()
            m = {}

            # get the course number from the course title if this is a Moodle integration
            #m = re.search("\[[(a-zA-Z0-9)]+\]", params['context_title'])

            if m:
                self.request.session['refering_course'] = m
            self.request.session['refering_section_code'] = params['context_label']
            self.request.session['refering_course_id'] = params['context_id']
            if self.is_instructor(tp):
                login(request, user)
                self.request.session['usertype'] = 'instructor'
                return redirect("IndexView")

            if self.is_student(tp):
                login(request, user)
                self.request.session['usertype'] = 'student'
                return redirect("IndexView")
            else:
                return HttpResponse("You must be an instructor or student.")
        else:
            return HttpResponse("INVALID")



# for debugging

def dprint(msg):
    if DEBUG == True:
        pprint(msg)