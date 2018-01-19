from django.test import TestCase, Client
from django.contrib.auth.models import User
from Mail2.models import Mail, Attachment, Route
import simplejson as json
from pprint import pprint
import datetime

class myTestCase(TestCase):

    def setUp(self):

        pass

    def test_LTI_can_login(self):
        c=Client



