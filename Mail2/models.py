from django.db import models
from django.contrib.auth.models import User
# Create your models here.


class Mail(models.Model):
    content = models.TextField()
    subject = models.CharField(max_length=512)
    fk_sender = models.ForeignKey(User)

    def __str__(self):
        return self.subject

class Attachment(models.Model):
    filepath = models.CharField(max_length=512)
    filename = models.CharField(max_length=1024)
    fk_mail = models.ForeignKey(Mail)

    def __str__(self):
        return self.filename

class Route(models.Model):
    fk_to = models.ForeignKey(User)
    read = models.BooleanField(default=False)
    fk_mail = models.ForeignKey(Mail)


