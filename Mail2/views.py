from django.shortcuts import render, HttpResponse,redirect, get_object_or_404, reverse
from django.http import JsonResponse
from django.views.generic import TemplateView, FormView, View
from .models import Route, Mail, Attachment
from django.db.models import Count
from django.contrib.auth.models import User
from Mail2proj.settings import DEBUG, MEDIA_ROOT,MAX_UPLOAD_SIZE
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
from hashlib import sha1
import magic
import os, tempfile, smtplib
from django.template.loader import render_to_string
from django.template import Context
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
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
            if route.archived is False:
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
                mail['attachments'] = Attachment.objects.filter(m2m_mail=message)
                # if Attachment.objects.filter(fk_mail=message):
                #     mail['has_attachment'] = True
                # else:
                #     mail['has_attachment'] = False
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
        for usermail in usermails:
            if not Mail.objects.filter(parent=usermail).exists():
                routes = Route.objects.filter(fk_mail=usermail)


                mail = {}
                for route in routes:

                    if 'to' in mail:
                        mail['to'] = mail['to'] + ', ' + route.to
                    else:
                        mail['to'] = route.to
                    if User.objects.filter(username=route.to).exists():
                        mail['userid'] = User.objects.get(username=route.to).id

                mail['id'] = usermail.id
                mail['subject'] = usermail.subject

                mail['termcode'] = usermail.termcode
                mail['section'] = usermail.section
                mail['date'] = str(usermail.created.month)+"/"+str(usermail.created.day)+"/"+str(usermail.created.year)
                mail['time'] = str(usermail.created.hour)+":"+str(usermail.created.minute)+":"+str(usermail.created.second)
                mail['timestamp'] = usermail.created.timestamp()
                #pprint(mail['date'])
                mail['from'] = usermail.fk_sender
                mail['attachments'] = Attachment.objects.filter(m2m_mail=usermail)
                email.append(mail)
        context['email'] = email
        context['session'] = self.request.session
        return context


class ComposeView(LoginRequiredMixin, FormView):
    template_name = 'compose.html'
    form_class = ComposeForm
    success_url = "/"
    raise_exception = True

    def form_invalid(self, form):
        pprint(form.errors)
        return super(ComposeView, self).form_invalid(form)

    def form_valid(self, form):
        recipients = self.request.POST.getlist('sendto')
        new_msg = Mail()
        new_msg.content = self.request.POST['content']
        new_msg.subject = self.request.POST['subject']
        new_msg.termcode = self.request.POST['termcode']
        new_msg.section = self.request.POST['section']
        new_msg.fk_sender = self.request.user
        new_msg.save()
        for recipient in recipients:
            new_route = Route()
            new_route.to = recipient
            new_route.fk_mail = new_msg
            new_route.save()
        attachments = self.request.POST.getlist('attachments')
        for item in attachments:
            attachment = Attachment.objects.get(id=item)
            attachment.m2m_mail.add(new_msg)
            attachment.save()
        build_email(new_msg, recipients)
        return super(ComposeView, self).form_valid(form)


    def get_context_data(self, **kwargs):

        context = super(ComposeView, self).get_context_data(**kwargs)
        if 'sn' in self.kwargs:
            context['sn'] = self.kwargs['sn']

        else:
            context['sn'] = 'False'

        context['session'] = self.request.session
        return context




class ReplyViewParent(LoginRequiredMixin, UserPassesTestMixin, FormView):

    template_name = 'reply.html'
    form_class = ReplyForm
    success_url = "/"
    # raise_exception = True
    login_url = 'http://localhost/mod/lti/view.php?id=3'

    def test_func(self, user):
        route = Route.objects.get(fk_mail=Mail.objects.get(pk=self.kwargs['id']), to=self.request.user.username)
        return self.request.user.username.lower() == route.to.lower()


    def get_initial(self, **kwargs):
        initial = super(ReplyViewParent, self).get_initial()
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
        new_msg.parent_id = self.kwargs['id']
        new_msg.fk_sender = self.request.user
        new_msg.save()
        new_route.to =self.request.POST['sendto']
        new_route.fk_mail = new_msg
        new_route.save()
        attachments = self.request.POST.getlist('attachments')
        pprint(attachments)
        for item in attachments:
            if item != "":
                attachment = Attachment.objects.get(id=item)
                attachment.m2m_mail.add(new_msg)
                attachment.save()
        build_email(new_msg, [self.request.POST['sendto']])
        return super(ReplyViewParent, self).form_valid(form)

    def get_context_data(self, **kwargs):
        context = super(ReplyViewParent, self).get_context_data(**kwargs)
        info = {}



        if Mail.objects.filter(id=self.kwargs['id']).exists():
            m = Mail.objects.get(id=self.kwargs['id'])
            # Make the parent list for threading
            parentlist = []
            parent = m.parent
            while parent is not None:
                p = {}
                p['id'] = parent.id
                p['fk_sender'] = parent.fk_sender
                p['subject'] = parent.subject
                p['created'] = parent.created
                p['content'] = parent.content
                p['attachments'] = Attachment.objects.filter(m2m_mail=parent)
                if Route.objects.filter(fk_mail=parent, to=self.request.user.username):
                    p['read'] = Route.objects.get(fk_mail=parent, to=self.request.user.username).read
                    p['routeid'] = Route.objects.get(fk_mail=parent, to=self.request.user.username).id
                else:
                    p['read'] = True
                parentlist.append(p)
                parent = parent.parent
            context['parentlist'] = list(reversed(parentlist))
            context['attachments'] = Attachment.objects.filter(m2m_mail=m)
            routes = Route.objects.filter(fk_mail=m)
            if m.fk_sender == self.request.user:
                for route in routes:
                    if 'to' in info:
                        info['to'] = info['to'] + ', ' + route.to
                    else:
                        info['to'] = route.to
            else:
                info['to'] = self.request.user.username

            if Route.objects.filter(fk_mail=m, to=self.request.user.username).exists():
                route = Route.objects.get(fk_mail=m, to=self.request.user.username)

            # print(info['to'])
            info['id'] = m.id
            info['content'] = m.content
            info['subject'] = m.subject
            info['termccode'] = m.termcode
            info['section'] = m.section
            info['fk_sender'] = m.fk_sender
            info['created'] = m.created
            info['timestamp'] = m.created.timestamp()
            info['parent'] = m.parent
            info['archived'] = route.archived
            if 'sn' in self.kwargs:
                info['referer'] = self.kwargs['sn']
            pprint("This is the reply view")
            pprint(info)
            context['mail'] = info
            # dprint(context)
        else:
            # todo raise error
            print("oh noes")
        context['session'] = self.request.session


        # Mark all the mail in this thread as read.


        return context

    def form_invalid(self, form):
        pprint(form.errors)
        return super(ReplyViewParent, self).form_invalid(form)


class ReplyView(ReplyViewParent):

    def get(self, request, *args, **kwargs):
        # print(User.objects.get(id=self.kwargs['userid']).username)
        route = Route.objects.get(fk_mail=Mail.objects.get(pk=self.kwargs['id']), to=User.objects.get(id=request.user.id))
        route.read = True
        route.save()
        return super(ReplyView, self).get(args, kwargs)

class OutboxReplyView(ReplyViewParent):

    def test_func(self, user):
        mail = Mail.objects.get(pk=self.kwargs['id'])
        return self.request.user == mail.fk_sender

    def get_initial(self, **kwargs):
        initial = super(OutboxReplyView, self).get_initial()
        if Mail.objects.filter(id=self.kwargs['id']).exists():
            mail_obj = Mail.objects.get(id=self.kwargs['id'])
            # router = Route.objects.get(fk_mail=mail_obj, to=User.objects.get(self.kwargs['userid']).username)

            data = {}
            data['sendto'] = User.objects.get(id=self.kwargs['userid']).username
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
            if Route.objects.filter(fk_mail=message, to=request.user.username).exists():
                route = Route.objects.get(fk_mail=message, to=request.user.username)
                route.archived = True
                route.save()
                if request.POST['referer'] != '00000-000S':
                    return redirect("/label/{}".format(request.POST['referer']))
                else:
                    return redirect("/")
            else:
                raise PermissionDenied
        else:
            raise PermissionDenied


class UnarchiveMailView(LoginRequiredMixin, View):
    raise_exception = True
    #TODO make redirect to prev page not /

    def post(self, request):

        if Mail.objects.filter(id=request.POST['message_id']).exists():
            message = Mail.objects.get(id=request.POST['message_id'])
            if Route.objects.filter(fk_mail=message, to=request.user.username).exists():
                route = Route.objects.get(fk_mail=message, to=request.user.username)
                route.archived = False
                route.save()
                if request.POST['referer'] != '00000-000S':
                    return redirect("/label/{}".format(request.POST['referer']))
                else:
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
            route = Route.objects.get(fk_mail=message, to=self.request.user.username)
            if request.user.username == route.to:
                route.read = False
                route.save()
                message.archived = False
                message.save()
                if request.POST['referer'] != '00000-000S':
                    return redirect("/label/{}".format(request.POST['referer']))
                else:
                    return redirect("/")
            else:
                raise PermissionDenied
        else:
            raise PermissionDenied


class AuditView(LoginRequiredMixin,GroupRequiredMixin,TemplateView):
    group_required = u"Auditor"
    template_name = 'audit.html'

    def get_context_data(self, **kwargs):
        context = super(AuditView, self).get_context_data(**kwargs)
        context['session'] = self.request.session
        return context


class AuditViewClass(AuditView, FormView):
    form_class = AuditClassForm

    def get_initial(self,**kwargs):
        initial = super(AuditViewClass, self).get_initial()
        return initial

    def get_context_data(self, **kwargs):
        context = super(AuditViewClass, self).get_context_data(**kwargs)
        data = []
        dataqs = Mail.objects.values('termcode').annotate(num_termcodes=Count('termcode'))
       # for row in dataqs:
       #     data.append(row["section"] + "-" + row["termcode"])
        dprint(str(dataqs.query))
        for flasdfc in dataqs:

            dprint(flasdfc)
        if 'termcode' in self.kwargs:
            courseqs = Mail.objects.filter(termcode=self.kwargs['termcode']).values('section').annotate(num_sections=Count('section'))
        else:
            courseqs = Mail.objects.filter(termcode="173s").values('section').annotate(
                num_sections=Count('section'))


        context['audit_termcodes'] = dataqs
        context['audit_class_list_for_term'] = courseqs
        dprint(context)
        return context


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
                mail['read'] = Route.objects.filter(fk_mail=message.id, to=self.request.user.username).get().read
                mail['termcode'] = message.termcode
                mail['section'] = message.section
                mail['date'] = str(message.created.month) + "/" + str(message.created.day) + "/" + str(message.created.year)
                mail['time'] = str(message.created.hour) + ":" + str(message.created.minute) + ":" + str(
                    message.created.second)
                mail['timestamp'] = message.created.timestamp()
                mail['attachments'] = Attachment.objects.filter(m2m_mail=message)
                # pprint(mail['date'])
                mail['from'] = message.fk_sender
                # if Attachment.objects.filter(fk_mail=message):
                #     mail['has_attachment'] = True
                # else:
                #     mail['has_attachment'] = False
                email.append(mail)
            context['email'] = email
            context['courses'] = courses
        context['session'] = self.request.session
        return context


class GetEmailListView(View):

    def get(self, *args, **kwargs):
        response = {}

        # if no sn is specified, get all of the routes for the user.
        if 'sn' not in self.kwargs:
            routes = Route.objects.filter(to=self.request.user)
        else:
            #get all of the routes to this user in this section
            section, termcode = self.kwargs['sn'].split('-')
            emails = Mail.objects.filter(section=section, termcode=termcode)
            routes = Route.objects.filter(fk_mail__in=emails, to=self.request.user.username)

        messages = []
        for route in routes:
            mail = route.fk_mail
            # if not Mail.objects.filter(parent=mail).exists():
            sender = {}
            sender['username'] = mail.fk_sender.username
            if mail.fk_sender.first_name is not None:
                sender['first_name'] = mail.fk_sender.first_name
            else:
                sender['first_name'] = ""
            if mail.fk_sender.last_name is not None:
                sender['last_name'] = mail.fk_sender.last_name
            else:
                sender['last_name'] = ""
            message = {
                'userid': self.request.user.id,
                'id': mail.id,
                'read': route.read,
                'from': sender,
                'archived': route.archived,
                # TODO if sent today, use just time, else just use date.  ("%I:%M %p")
                'timestamp': mail.created.strftime("%m/%d/%Y"),
                'section':  mail.section,
                'subject': mail.subject,
                }
            if Attachment.objects.filter(m2m_mail=mail).exists():
                message['attachments'] = True
            else:
                message['attachments'] = False
            messages.append(message)
            if 'sn' in self.kwargs:
                response = {'inbox': True, 'messages': list(reversed(messages)) }
            else:
                response = {'inbox': False, 'messages': list(reversed(messages))}
        return HttpResponse(json.dumps(response), content_type="application/json")




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
        return HttpResponse(json.dumps(results), content_type="application/json")


class DownloadView(UserPassesTestMixin, View):

    def test_func(self, user):
        attachment = get_object_or_404(Attachment, id=self.kwargs['pk'])
        mails = attachment.m2m_mail.all()
        for mail in mails:
            if mail.fk_sender == user:
                return True
            else:
                routes = Route.objects.filter(fk_mail=mail)
                for route in routes:
                    if route.to == user.username:
                        return True
        return False

    def get(self, request, **kwargs):

        attachment = get_object_or_404(Attachment, pk=self.kwargs['pk'])
        file = open(attachment.filepath, 'rb')
        mime = magic.from_file(attachment.filepath)
        pprint(mime)
        response = HttpResponse(file.read(), content_type=mime)
        response['Content-Disposition'] = 'attachment; filename={}'.format(attachment.filename)
        return response


class FileUpload(LoginRequiredMixin, View):

    def post(self, *args, **kwargs):

        file = self.request.FILES['attachment']
        tempdir = tempfile.gettempdir() + '/'
        fp = open(tempdir + self.request.session.session_key, 'w+b')
        for chunk in file.chunks():
            fp.write(chunk)
        fp.close()

        fp = open(tempdir + self.request.session.session_key, 'rb')
        hash_of_file = hash_file(fp)
        fp.close()

        if not os.path.isfile(MEDIA_ROOT + hash_of_file):
            # move temp file to media
            os.rename(tempdir + self.request.session.session_key,
                      MEDIA_ROOT + hash_of_file)
        new_attachment = Attachment()
        new_attachment.filename = file.name
        new_attachment.filepath = MEDIA_ROOT + hash_of_file
        new_attachment.hashedname = hash_of_file
        new_attachment.save()
        res = {"success": True, "error": "", "filename": file.name, "attachment_id": new_attachment.id }
        return JsonResponse(res)



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
                if 'custom_redirect' in params:
                    return redirect(params['custom_redirect'])
                return redirect("IndexView")

            if self.is_student(tp):
                login(request, user)
                self.request.session['usertype'] = 'student'
                if 'custom_redirect' in params:
                    return redirect(params['custom_redirect'])
                return redirect("IndexView")
            else:
                return HttpResponse("You must be an instructor or student.")
        else:
            return HttpResponse("INVALID")



def hash_file(fp, buffer_size=65536):
    '''
    hash a file contents with sha1
    :param fp: file pointer to file opened in rb
    :param buffer_size: 65536 by default
    :return: sha1 hexdigest
    '''


    hash = sha1()

    while 1:
        data = fp.read(buffer_size)
        if not data:
            break
        hash.update(data)

    return hash.hexdigest()



# for debugging

def dprint(msg):
    if DEBUG == True:
        pprint(msg)


def build_email(msg_form, destinations):
    cont = {}

    for destination in destinations:

        receiver = User.objects.get(username=destination)

        to = {'first_name':receiver.first_name,
              'last_name':receiver.last_name,
              'email_address':receiver.email,
              }

        sender = {'first_name': msg_form.fk_sender.first_name,
                'last_name': msg_form.fk_sender.last_name }

        mail = {'to': to,
                'sender': sender,
                'userid': receiver.id,
                'section':msg_form.section,
                'subject':msg_form.subject,
                'content':msg_form.content,
                'id': msg_form.id,
                'sectioncode': "{}-{}".format(msg_form.section,msg_form.termcode)
                }

        cont = {'server_url': 'https://mail2.wosc.edu',
                'mail':mail }

        html_email = render_to_string("email_the_mail_html.html", cont)
        text_email = render_to_string("email_the_mail_text.txt", cont)
        part1 = MIMEText(text_email, 'plain')
        part2 = MIMEText(html_email, 'html')
        msg = MIMEMultipart('alternative')
        msg['Subject'] = '📧 New MoodleMail from course: {} new'.format(msg_form.section)
        msg['From'] = 'NoReply_MoodleMail@wosc.edu'
        msg['To'] = to['email_address']
        msg.attach(part1)
        msg.attach(part2)
        send_email(msg, to['email_address'])


def send_email(msg, destination):
    email_server = smtplib.SMTP("10.250.20.169")
    email_server.sendmail(msg=msg.as_string(), from_addr='NoReply_MoodleMail@wosc.edu', to_addrs=destination)

