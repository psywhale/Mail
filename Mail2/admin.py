from django.contrib import admin
from .models import *

class RouteAdmin(admin.ModelAdmin):
    list_display = ['fk_to', 'read', 'fk_mail']

class MailAdmin(admin.ModelAdmin):
    list_display = ['fk_sender', 'subject']

class AttachmentAdmin(admin.ModelAdmin):
    list_display = ['filename', 'fk_mail']

# Register your models here.
admin.site.register(Route, RouteAdmin)
admin.site.register(Mail, MailAdmin)
admin.site.register(Attachment, AttachmentAdmin)
