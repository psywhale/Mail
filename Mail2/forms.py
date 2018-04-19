from django import forms
from .models import Attachment, Mail, Route, User




class ReplyForm(forms.Form):
    sendto = forms.CharField(widget=forms.HiddenInput)
    content = forms.CharField(widget=forms.Textarea(attrs={"class": "reply_editor"}), required=False)
    subject = forms.CharField(widget=forms.HiddenInput, required=False)
    termcode = forms.CharField(widget=forms.HiddenInput)
    section = forms.CharField(widget=forms.HiddenInput)
    attachments = forms.CharField(widget=forms.HiddenInput)
    def clean(self):
        self.check_file()
        return self.cleaned_data

    def check_file(self):
        content = self.cleaned_data["attachments"]



class ComposeForm(ReplyForm):
    sendto = forms.CharField(widget=forms.Select(), initial="")
    subject = forms.CharField(widget=forms.TextInput(), max_length=510, required=False )

class AuditClassForm(forms.Form):
    audit_class = forms.ChoiceField(widget=forms.Select(), initial="")

class AuditUserForm(forms.Form):
    audit_user = forms.ChoiceField(widget=forms.Select(), initial="")


