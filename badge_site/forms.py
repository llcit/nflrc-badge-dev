# forms.py
from django.forms import ModelForm
# from django import forms

from badge_site.models import Issuer, Badge, Award

class CreateIssuerForm(ModelForm):
    class Meta:
        model = Issuer
        fields = ['name', 'initials', 'url', 'doc_path', 'desc', 'image', 'contact']
        # widgets = {'guid':forms.HiddenInput()}  

class CreateBadgeForm(ModelForm):
    class Meta:
        model = Badge
        fields = ['name', 'image', 'description', 'criteria', 'issuer']
        # widgets = {'guid':forms.HiddenInput()}  

class CreateAwardForm(ModelForm):
    class Meta:
        model = Award
        fields = ['email', 'firstname', 'lastname', 'badge', 'creator', 'evidence', 'expires']
        # widgets = {'guid':forms.HiddenInput()}


