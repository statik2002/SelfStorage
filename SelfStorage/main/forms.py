from django import forms
from django.forms.widgets import DateInput
from .models import City


class loginForm(forms.Form):
    email = forms.EmailField()
    password = forms.PasswordInput()


class CalcForm(forms.Form):
    city = forms.ModelChoiceField(
        label='Выберите город',
        localize=True,
        queryset=City.objects.all(),
        required=True,
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    square = forms.DecimalField(label='Какая площадь необходима', decimal_places=1, max_digits=3, min_value=1.5)
    start_date = forms.DateField(label='Начала использования', widget=DateInput(attrs={'type': 'date'}))
    end_date = forms.DateField(label='Окончание использования', widget=DateInput(attrs={'type': 'date'}))
    delivery = forms.BooleanField(label='Доставка', required=False)
    loaders = forms.BooleanField(label='Грузчики', required=False)
