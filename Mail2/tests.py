from django.test import TestCase, Client
from django.contrib.auth.models import User
from .models import Mail, Attachment, Route

# Create your tests here.

class InboxTest(TestCase):
    def setUp(self):
        userfrom=User.objects.create_user(username='TestPerson',
                                 password='whatevs',
                                 first_name='Testislez',
                                 last_name='Person')
        userto = User.objects.create_user(username='Ned',
                                            password='whatevas',
                                            first_name='Ned',
                                            last_name='Person')
        mailmsg = Mail.objects.create(content='Test Message',
                            subject='test subject',
                            fk_sender=userfrom)

        Route.objects.create(fk_to=userto,
                             read=False,
                             fk_mail=mailmsg)

        Attachment.objects.create(filepath='/mnt/maildata',
                                  filename='tatadfa.doc',
                                  fk_mail=mailmsg
                                  )
    def bad_users_have_no_access(self):
        c=Client()
        res=c.get('/')
        self.assertEqual(res.status_code, 403)

