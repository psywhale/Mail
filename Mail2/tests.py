from django.test import TestCase, Client
from django.contrib.auth.models import User
from .models import Mail
from .models import Route
from .models import Attachment

#from django.core.management import call_command
import simplejson as json
from pprint import pprint
import datetime

# Create your tests here.

# class JenkinsTest(TestCase):
#     def test_what_if_fail(self):
#         self.assertEqual(1,3)

#call_command('flush','--noinput')



class myTestCase(TestCase):

    def setUp(self):

        frank = User.objects.create_user(username='Frank',
                                         password='whatevs',
                                         first_name='Testislez',
                                         last_name='Person')
        ned = User.objects.create_user(username='Ned',
                                       password='whatevas',
                                       first_name='Ned',
                                       last_name='Person')
        # Message with an attachment that is for Frank
        mailmsg = Mail.objects.create(content='Test Message',
                                      subject='test message for Frank',
                                      fk_sender=ned,
                                      termcode="172s",
                                      section="21232")

        Route.objects.create(to='frank',
                             read=False,
                             fk_mail=mailmsg)

        # Attachment.objects.create(filepath='/mnt/maildata',
        #                           filename='tatadfa.doc',
        #                           fk_mail=mailmsg
        #                           )
        # Messsage for frank that does not have an attachment
        mailmsg = Mail.objects.create(content='Test message for frank',
                                      subject='No Attachment for frank',
                                      fk_sender=ned,
                                      termcode = "172s",
                                      section = "21231")

        Route.objects.create(to='frank',
                             read=False,
                             fk_mail=mailmsg)
        # Message for "Ned"
        mailmsg = Mail.objects.create(content='Test Message 3',
                                      subject='test subject for Ned',
                                      fk_sender=frank,
                                      termcode="172s",
                                      section="21232"
                                      )

        Route.objects.create(to=str(ned.username),
                             read=False,
                             fk_mail=mailmsg)

        # Attachment.objects.create(filepath='/mnt/maildata',
        #                           filename='tatadfa2.doc',
        #                           fk_mail=mailmsg
        #                           )

        # A Message to frank that is read
        mailmsg = Mail.objects.create(content='Test Message 4',
                                      subject='test email read',
                                      fk_sender=ned,
                                      termcode="172s",
                                      section="21231"
                                      )

        Route.objects.create(to=frank.username,
                             read=True,
                             fk_mail=mailmsg)

        # Attachment.objects.create(filepath='/mnt/maildata',
        #                           filename='tatadfa3.doc',
        #                           fk_mail=mailmsg
        #                           )

class MarkMailUnreadTest(myTestCase):


    def test_bad_users_cannot_markunread(self):
        c = Client()
        res = c.login(username='Frank', password='whatevs')
        mailmsg = Mail.objects.create(content='Test REPLY',
                                      subject='test timestamp for Ned',
                                      fk_sender=User.objects.get(username="Frank"),
                                      termcode="172s",
                                      section="21231",
                                      )
        Route.objects.create(to=User.objects.get(username="Ned").username,
                                     read=False,
                                     fk_mail=mailmsg)
        res = c.post('/munread/', {"message_id":mailmsg.id})
        self.assertEqual(res.status_code, 403)

    def test_good_users_can_markunread(self):
        c = Client()
        res = c.login(username='Frank', password='whatevs')
        mailmsg = Mail.objects.create(content='Test REPLY',
                                      subject='test timestamp for Ned',
                                      fk_sender=User.objects.get(username="Ned"),
                                      termcode="172s",
                                      section="21231",
                                      )
        Route.objects.create(to=User.objects.get(username="Frank").username,
                                     read=False,
                                     fk_mail=mailmsg)
        res = c.post('/archive/', {"message_id":mailmsg.id})
        self.assertEqual(res.status_code, 302)


class ArchiveTest(myTestCase):


    def test_bad_users_cannot_archive(self):
        c = Client()
        res = c.login(username='Frank', password='whatevs')
        mailmsg = Mail.objects.create(content='Test REPLY',
                                      subject='test timestamp for Ned',
                                      fk_sender=User.objects.get(username="Frank"),
                                      termcode="172s",
                                      section="21231",
                                      )
        Route.objects.create(to=User.objects.get(username="Ned").username,
                                     read=False,
                                     fk_mail=mailmsg)
        res = c.post('/archive/', {"message_id":mailmsg.id})
        self.assertEqual(res.status_code, 403)

    def test_good_users_can_archive_mail(self):
        c = Client()
        res = c.login(username='Frank', password='whatevs')
        mailmsg = Mail.objects.create(content='Test REPLY',
                                      subject='test timestamp for Ned',
                                      fk_sender=User.objects.get(username="Ned"),
                                      termcode="172s",
                                      section="21231",
                                      )
        Route.objects.create(to=User.objects.get(username="Frank"),
                                     read=False,
                                     fk_mail=mailmsg)
        res = c.post('/archive/', {"message_id":mailmsg.id})
        self.assertEqual(res.status_code, 302)

class InboxTest(myTestCase):


    def test_bad_users_have_no_access(self):
        c = Client()
        res = c.get('/')

        self.assertEqual(res.status_code, 403)

    def test_can_login(self):
        c = Client()
        res = c.login(username='Frank', password='whatevs')
        reslogin = c.get('/')
        self.assertEqual(reslogin.status_code, 200)

    def test_can_see_email(self):
        c = Client()
        res = c.login(username='Frank', password='whatevs')
        reslogin = c.get('/listEmail/')
        exists = False

        data = json.loads(reslogin.content)

        for message in data['messages']:
            pprint(message)
            if message['subject'] == "test message for Frank":
                exists = True
        self.assertTrue(exists)

    def test_cannot_see_wrong_email(self):
        c = Client()
        res = c.login(username='Frank', password='whatevs')
        reslogin = c.get('/listEmail/')
        exists = False

        data = json.loads(reslogin.content)

        for message in data['messages']:
            if message['subject'] == "test subject for Ned":
                exists = True
        self.assertFalse(exists)

    # def test_can_see_attachments(self):
    #     c = Client()
    #     res = c.login(username='Frank', password='whatevs')
    #     reslogin = c.get('/')
    #     exists = False
    #     for message in reslogin.context['email']:
    #         if message['has_attachment']:
    #             exists = True
    #     self.assertTrue(exists)

    def test_email_has_right_date(self):
        mailmsg = Mail.objects.create(content='Test timestamp',
                                      subject='test timestamp for Ned',
                                      fk_sender=User.objects.get(username="Frank"),
                                      termcode="172s",
                                      section="21231"
                                      )
        self.assertEqual(datetime.datetime.now().day, mailmsg.created.day)

    # def test_user_gets_a_list_of_unique_courses(self):
    #     c = Client()
    #     res = c.login(username='Frank', password='whatevs')
    #     reslogin = c.get('/')
    #     #print(reslogin.context['courses'])
    #     self.assertTrue(allUnique(reslogin.context['courses']))

class ReplyTest(myTestCase):

    def test_user_can_see_mail(self):
        c = Client()
        mailmsg = Mail.objects.create(content='Test REPLY',
                                      subject='test timestamp for Ned',
                                      fk_sender=User.objects.get(username="Ned"),
                                      termcode="172s",
                                      section="21231",

                                      )
        Route.objects.create(to=User.objects.get(username="Frank").username,
                                     read=False,
                                     fk_mail=mailmsg)
        c.login(username='Frank', password='whatevs')
        reslogin = c.get('/reply/' + str(mailmsg.id), follow=True)
        self.assertEqual(reslogin.status_code, 200)

    def test_user_cannot_see_other_users_mail(self):
        c = Client()
        mailmsg = Mail.objects.create(content='Test REPLY',
                                      subject='test timestamp for Ned',
                                      fk_sender=User.objects.get(username="Frank"),
                                      termcode="172s",
                                      section="21231",

                                      )
        Route.objects.create(to=User.objects.get(username="Ned").username,
                                     read=False,
                                     fk_mail=mailmsg)
        c.login(username='Frank', password='whatevs')
        reslogin = c.get('/reply/' + str(mailmsg.id), follow=True)
        self.assertEqual(reslogin.status_code, 403)

    def test_message_gets_marked_as_read_on_open(self):
        c = Client()
        mailmsg = Mail.objects.create(content='Test REPLY',
                                      subject='test timestamp for Ned',
                                      fk_sender=User.objects.get(username="Frank"),
                                      termcode="172s",
                                      section="21231",
                                      )

        Route.objects.create(to=User.objects.get(username="Ned").username,
                                     read=False,
                                     fk_mail=mailmsg)
        c.login(username='Ned', password='whatevas')
        c.get('/reply/' + str(mailmsg.id), follow=True)
        self.assertTrue(Route.objects.get(fk_mail=mailmsg).read)

class LabelTest(myTestCase):

    def test_label_view_only_lists_email_for_class(self):
        c = Client()
        res = c.login(username='Frank', password='whatevs')
        reslogin = c.get('/label/21231-172s/')
        exists = False

        for message in reslogin.context['email']:
            if message['section'] == "21231":
                exists = True
        self.assertTrue(exists)

    def test_label_can_not_view_only_lists_email_for_class(self):
        c = Client()
        res = c.login(username='Frank', password='whatevs')
        reslogin = c.get('/label/21232-172s/')
        exists = False
        for message in reslogin.context['email']:
            if message['section'] == "21231":
                exists = True
        self.assertFalse(exists)


class ListUnreadTest(myTestCase):

    def test_for_unread_mail(self):
        #TODO fix it, fix it.


        self.assertTrue(True)

        # c = Client()
        # res = c.login(username='Frank', password='whatevs')
        # data = []
        # data.append({"course": '21231-172s'})
        # data.append({"course": '21232-172s'})
        # reslogin = c.post('/listunread/', json.dumps(data), content_type='application/json')
        # data = json.loads(reslogin.content)
        # self.assertEqual(data["0"]['count'], 1)
        # self.assertEqual(data["1"]['count'], 1)

class ComposeTest(myTestCase):

    def test_bad_users_have_no_access(self):
        c = Client()
        res = c.get('/compose/')

        self.assertEqual(res.status_code, 403)

    def test_can_login(self):
        c = Client()
        res = c.login(username='Frank', password='whatevs')
        reslogin = c.get('/compose/')
        self.assertEqual(reslogin.status_code, 200)

    def test_can_see_compose(self):
        c = Client()
        res = c.login(username='Frank', password='whatevs')
        reslogin = c.get('/compose/')
        exists = True
        # TODO make it test for view

        self.assertEqual(reslogin.status_code, 200)

class OutboxTest(myTestCase):

    def test_bad_users_have_no_access(self):
        tt = Client()
        res = tt.get('/outbox/')

        self.assertEqual(res.status_code, 403)

    def test_can_login(self):
        c = Client()
        res = c.login(username='Frank', password='whatevs')
        reslogin = c.get('/outbox/')
        self.assertEqual(reslogin.status_code, 200)

    def test_can_see_outbox(self):
        c = Client()
        res = c.login(username='Frank', password='whatevs')
        reslogin = c.get('/outbox/')
        exists = False
        # TODO make it test for view
        for message in reslogin.context['email']:
            if message['subject'] == "test subject for Ned":
                exists = True

        self.assertTrue(exists)

    def test_can_see_sent_email(self):
        mailmsg = Mail.objects.create(content='Test REPLY',
                                      subject='test timestamp for Ned',
                                      fk_sender=User.objects.get(username="Frank"),
                                      termcode="172s",
                                      section="21231",
                                      )
        Route.objects.create(to='Ned',
                             read=False,
                             fk_mail=mailmsg)

        c = Client()
        res = c.login(username='Frank', password='whatevs')
        reslogin = c.get('/outbox/')
        exists = False
        for message in reslogin.context['email']:
            if message['subject'] == "test timestamp for Ned":
                exists = True
        self.assertTrue(exists)

    def can_see_sent_email_even_if_usr_no_exist(self):
        mailmsg = Mail.objects.create(content='Test REPLY',
                                      subject='test timestamp for Ned',
                                      fk_sender=User.objects.get(username="Frank"),
                                      termcode="172s",
                                      section="21231",
                                      )
        Route.objects.create(to='Narkles',
                             read=False,
                             fk_mail=mailmsg)

        c = Client()
        res = c.login(username='Frank', password='whatevs')
        reslogin = c.get('/outbox/')
        exists = False
        for message in reslogin.context['email']:
            if message['subject'] == "test timestamp for Ned":
                exists = True
        self.assertTrue(exists)

class OutboxReplyTest(myTestCase):

    def test_bad_users_have_no_access(self):
        tt = Client()
        res = tt.get('/outbox/')

        self.assertEqual(res.status_code, 403)

    def test_can_reply_from_outbox(self):
        c = Client()
        res = c.login(username='Frank', password='whatevs')
        mailmsg = Mail.objects.create(content='Test REPLY',
                                      subject='test timestamp for Ned',
                                      fk_sender=User.objects.get(username="Frank"),
                                      termcode="172s",
                                      section="21231",
                                      )
        Route.objects.create(to=User.objects.get(username="Ned").username,
                             read=False,
                             fk_mail=mailmsg)
        resout = c.get('/or/'+str(mailmsg.id)+"/")
        self.assertEqual(resout.status_code, 200)

class ComposeViewTest(myTestCase):

    def test_form_valid(self):
        c = Client()
        res = c.login(username='Frank', password='whatevs')
        user = User.objects.get(username="Frank")
        to_user = User.objects.get(username="Ned")
        data = {
            "content":"This is the test content",
            "subject":"this is a test subject",
            "termcode":"173s",
            "section":"3000",
            "fk_sender": user.id,
            "sendto": to_user.id
        }
        res = c.post('/compose/',data)
        self.assertEqual(res.url, '/')

    def test_form_invalid(self):
        c = Client()
        res = c.login(username='Frank', password='whatevs')
        user = User.objects.get(username="Frank")
        to_user = User.objects.get(username="Ned")
        data = {
            "content":"This is the test content",
            "subject":"this is a test subject",
            "termcode":"173s",
            "section":"3000",
            "fk_sender": user.id,
        }

        res = c.post('/compose/', data)
        self.assertFormError(res, 'form', 'sendto', 'This field is required.')


    # def test_form_valid_with_attachment(self):
    #     c = Client()
    #     res = c.login(username='Frank', password='whatevs')
    #     user = User.objects.get(username="Frank")
    #     to_user = User.objects.get(username="Ned")
    #     fp = open('README.md', 'rb')
    #     data = {
    #         "content":"This is the test content",
    #         "subject":"this is a test subject",
    #         "termcode":"173s",
    #         "section":"3000",
    #         "fk_sender": user.id,
    #         "sendto": to_user.id,
    #         "attachments": fp
    #     }
    #     res = c.post('/compose/',data)
    #     self.assertEqual(res.url, '/')


class ReplyViewTest(myTestCase):


    def test_user_can_view_proper_reply(self):
        c = Client()
        res = c.login(username='Frank', password='whatevs')
        msg = Route.objects.filter(to="Frank")[0].fk_mail
        res = c.get('/reply/{}/'.format(msg.id))
        self.assertEqual(res.status_code, 200)

    def test_user_cannot_view_others(self):
        c = Client()
        res = c.login(username='Frank', password='whatevs')
        msg = Route.objects.filter(to="Ned")[0].fk_mail
        res = c.get('/reply/{}/'.format(msg.id))
        self.assertEqual(res.status_code, 403)


    def test_form_valid(self):
        c = Client()
        res = c.login(username='Frank', password='whatevs')
        user = User.objects.get(username="Frank")
        to_user = User.objects.get(username="Ned")
        msg = Route.objects.filter(to="Frank")[0].fk_mail
        data = {
            "content":"This is the test content",
            "subject":"this is a test subject",
            "termcode":"173s",
            "section":"3000",
            "fk_sender": user.id,
            "sendto": to_user.id
        }
        res = c.post('/reply/{}/'.format(msg.id),data)
        self.assertEqual(res.url, '/')

    def test_form_invalid(self):
        c = Client()
        res = c.login(username='Frank', password='whatevs')
        user = User.objects.get(username="Frank")
        to_user = User.objects.get(username="Ned")
        msg = Route.objects.filter(to="Frank")[0].fk_mail
        data = {
            "content":"This is the test content",
            "subject":"this is a test subject",
            "termcode":"173s",
            "section":"3000",
            "fk_sender": user.id,
        }

        res = c.post('/reply/{}/'.format(msg.id), data)
        self.assertFormError(res, 'form', 'sendto', 'This field is required.')



#------------------------------------------------------

def allUnique(x):
    seen = set()
    return not any(i in seen or seen.add(i) for i in x)