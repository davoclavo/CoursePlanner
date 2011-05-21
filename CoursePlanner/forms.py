from django import forms 
import re

class LoginForm(forms.Form):
    username = forms.CharField(
        label='KAIST Mail ID',
        max_length=20
    ) 
    password = forms.CharField(
        label='Password',
        initial='Password',
        widget=forms.PasswordInput()
    )
    
    def clean_username(self):
        username = self.cleaned_data['username']
        if re.search(r'^\w+$', username):
            return username
        else:
            raise forms.ValidationError('Username can only contain alphanumeric characters and underscores')
    
    """def clean_password(self):
        password = self.cleaned_data['password']
        return password"""

class SMSForm(forms.Form):

    fromhp = forms.CharField(
        label='From #',
        max_length=11,
    ) 
    
    tohp = forms.CharField(
        label='To #',
        max_length=11,
    )
    
    msg = forms.CharField(
        label='Message',
        max_length=80,
        widget = forms.Textarea
    )
    
    def clean_fromhp(self):
        number = self.cleaned_data['fromhp']
        if re.search(r'^010', number):
            return number
        else:
            raise forms.ValidationError('Number has to start with 010')
    
    def clean_tohp(self):
        number = self.cleaned_data['tohp']
        if re.search(r'^010', number):
            return number
        else:
            raise forms.ValidationError('Number has to start with 010')