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
