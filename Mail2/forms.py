from django import forms
from .models import Attachment, Mail, Route, User


class ReplyForm(forms.Form):
    sendto = forms.CharField(widget=forms.HiddenInput)
    content = forms.CharField(widget=forms.Textarea(attrs={"class": "reply_editor"}))
    subject = forms.CharField(widget=forms.HiddenInput)
    termcode = forms.CharField(widget=forms.HiddenInput)
    section = forms.CharField(widget=forms.HiddenInput)
    attachment = forms.FileField(widget=forms.FileInput,required=False)


class ComposeForm(ReplyForm):
    sendto = forms.CharField(widget=forms.Select(), initial="")
    subject = forms.CharField(widget=forms.TextInput(), max_length=510)

class AuditClassForm(forms.Form):
    audit_class = forms.ChoiceField(widget=forms.Select(), initial="")

class AuditUserForm(forms.Form):
    audit_user = forms.ChoiceField(widget=forms.Select(), initial="")


