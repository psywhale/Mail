from django.test import TestCase, Client
from django.contrib.auth.models import User
from .models import Mail, Attachment, Route
import datetime


# Create your tests here.

class InboxTest(TestCase):
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

        Route.objects.create(fk_to=frank,
                             read=False,
                             fk_mail=mailmsg)

        Attachment.objects.create(filepath='/mnt/maildata',
                                  filename='tatadfa.doc',
                                  fk_mail=mailmsg
                                  )
        # Messsage for frank that does not have an attachment
        mailmsg = Mail.objects.create(content='Test message for frank',
                                      subject='No Attachment for frank',
                                      fk_sender=ned,
                                      termcode = "172s",
                                      section = "21231")

        Route.objects.create(fk_to=frank,
                             read=False,
                             fk_mail=mailmsg)
        # Message for "Ned"
        mailmsg = Mail.objects.create(content='Test Message 3',
                                      subject='test subject for Ned',
                                      fk_sender=frank,
                                      termcode="172s",
                                      section="21232"
                                      )

        Route.objects.create(fk_to=ned,
                             read=False,
                             fk_mail=mailmsg)

        Attachment.objects.create(filepath='/mnt/maildata',
                                  filename='tatadfa2.doc',
                                  fk_mail=mailmsg
                                  )

        # A Message to frank that is read
        mailmsg = Mail.objects.create(content='Test Message 4',
                                      subject='test email read',
                                      fk_sender=ned,
                                      termcode="172s",
                                      section="21231"
                                      )

        Route.objects.create(fk_to=frank,
                             read=True,
                             fk_mail=mailmsg)

        Attachment.objects.create(filepath='/mnt/maildata',
                                  filename='tatadfa3.doc',
                                  fk_mail=mailmsg
                                  )

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
        reslogin = c.get('/')
        exists = False
        for message in reslogin.context['email']:
            if message['subject'] == "test message for Frank":
                exists = True
        self.assertTrue(exists)

    def test_cannot_see_wrong_email(self):
        c = Client()
        res = c.login(username='Frank', password='whatevs')
        reslogin = c.get('/')
        exists = False
        for message in reslogin.context['email']:
            if message['subject'] == "test subject for Ned":
                exists = True
        self.assertFalse(exists)

    def test_can_see_attachments(self):
        c = Client()
        res = c.login(username='Frank', password='whatevs')
        reslogin = c.get('/')
        exists = False
        for message in reslogin.context['email']:
            if message['has_attachment']:
                exists = True
        self.assertTrue(exists)

    def test_email_has_right_date(self):
        mailmsg = Mail.objects.create(content='Test timestamp',
                                      subject='test timestamp for Ned',
                                      fk_sender=User.objects.get(username="Frank"),
                                      termcode="172s",
                                      section="21231"
                                      )
        self.assertEqual(datetime.datetime.now().day, mailmsg.created.day)

    def test_user_gets_a_list_of_unique_courses(self):
        c = Client()
        res = c.login(username='Frank', password='whatevs')
        reslogin = c.get('/')
        print(reslogin.context['courses'])
        self.assertTrue(allUnique(reslogin.context['courses']))

    def test_can_see_individual_mail(self):
        c = Client()
        mailmsg = Mail.objects.create(content='Test REPLY',
                                      subject='test timestamp for Ned',
                                      fk_sender=User.objects.get(username="Frank"),
                                      termcode="172s",
                                      section="21231",
                                      fk_to=User.objects.get(username="Ned")
                                      )
        res = c.login(username='Frank', password='whatevs')
        reslogin = c.get('/read/'+mailmsg.id)


def allUnique(x):
    seen = set()
    return not any(i in seen or seen.add(i) for i in x)