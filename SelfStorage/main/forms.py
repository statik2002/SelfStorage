from django import forms


class loginForm(forms.Form):
    email = forms.EmailField()
    password = forms.PasswordInput()
