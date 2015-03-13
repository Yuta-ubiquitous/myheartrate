# -*- coding: utf-8 -*-
from django import forms
from django.contrib.auth import authenticate

class UploadFileForm(forms.Form):
    title = forms.CharField(max_length=50)
    file = forms.FileField()

class Login_form(forms.Form):
    username = forms.CharField(label="User name")
    password = forms.CharField(label="Password", widget=forms.PasswordInput)
    def clean(self):
        cleand_data = super(Login_form, self).clean()
        username = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')
        if not authenticate(username=username, password=password):
            raise forms.ValidationError("Wrong user name or password")
        return self.cleaned_data
