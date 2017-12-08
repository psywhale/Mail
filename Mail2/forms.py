from django import forms
from .models import Attachment, Mail, Route, User


class ReplyForm(forms.Form):
    sendto = forms.CharField(widget=forms.HiddenInput)
    content = forms.CharField(widget=forms.Textarea(attrs={"class": "reply_editor"}))
    subject = forms.CharField(widget=forms.HiddenInput)
    termcode = forms.CharField(widget=forms.HiddenInput)
    section = forms.CharField(widget=forms.HiddenInput)



