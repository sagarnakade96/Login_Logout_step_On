from django import forms
from django.forms import ModelForm, fields
from .models import Account

class AccountForm(ModelForm):
    class Meta:
        model = Account
        fields = ['name','email']
        