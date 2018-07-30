from django.db import models
from django.contrib.auth.models import User
# Create your models here.


class Mail(models.Model):
    content = models.TextField()
    subject = models.CharField(max_length=512)
    termcode = models.CharField(max_length=4)
    section = models.CharField(max_length=5)
    fk_sender = models.ForeignKey(User)
    created = models.DateTimeField(auto_now_add=True)
    parent = models.ForeignKey('self', null=True, blank=True)

    def __str__(self):
        return self.subject

class Attachment(models.Model):
    filepath = models.CharField(max_length=512)
    filename = models.CharField(max_length=1024)
    hashedname = models.CharField(max_length=40)
    m2m_mail = models.ManyToManyField(Mail)

    def __str__(self):
        return self.filename

class Route(models.Model):
    to = models.CharField(max_length=300, default="")
    read = models.BooleanField(default=False)
    fk_mail = models.ForeignKey(Mail)
    archived = models.BooleanField(default=False)

