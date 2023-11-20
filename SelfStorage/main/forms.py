from django import forms
from django.forms.widgets import DateInput
from phonenumber_field.formfields import PhoneNumberField
from .models import City


class loginForm(forms.Form):
    email = forms.EmailField()
    password = forms.PasswordInput()


class CalcForm(forms.Form):
    city = forms.ModelChoiceField(
        label='Выберите город',
        localize=True,
        queryset=City.objects.all(),
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    square = forms.DecimalField(label='Какая площадь необходима', decimal_places=1, max_digits=3, min_value=1.5)
    start_date = forms.DateField(label='Начала использования', widget=DateInput(attrs={'type': 'date'}))
    end_date = forms.DateField(label='Окончание использования', widget=DateInput(attrs={'type': 'date'}))
    delivery = forms.BooleanField(label='Доставка', required=False)
    loaders = forms.BooleanField(label='Грузчики', required=False)
    measurement = forms.BooleanField(label='Замерщик', required=False)


class CallBackOrderForm(forms.Form):
    phone = PhoneNumberField(label='Ваш телефон', region='RU', widget=forms.NumberInput(attrs={'class': 'form-control border-8 mb-4 py-3 px-5 border-0 fs_24 SelfStorage__bg_lightgrey'}))
    first_name = forms.CharField(label='Ваше имя', widget=forms.TextInput(attrs={'class': 'form-control border-8 mb-4 py-3 px-5 border-0 fs_24 SelfStorage__bg_lightgrey'}))
    last_name = forms.CharField(label='Ваша фамилия', widget=forms.TextInput(attrs={'class': 'form-control border-8 mb-4 py-3 px-5 border-0 fs_24 SelfStorage__bg_lightgrey'}))


class OrderForm(forms.Form):
    # address = forms.CharField(
    #     label='Адрес',
    #     required=False,
    #     max_length=100
    # )
    text = forms.CharField(label='Прмечание', required=False, widget=forms.Textarea)


class RegistrationForm(forms.Form):
    email = forms.EmailField(
        label='',
        max_length=255,
        widget=forms.EmailInput(attrs={
            'class': 'form-control border-8 mb-4 py-3 px-5 border-0 fs_24 SelfStorage__bg_lightgrey',
            'placeholder': 'Ваш email'
        })
    )
    first_name = forms.CharField(
        label='',
        max_length=255,
        widget=forms.TextInput(attrs={
            'class': 'form-control border-8 mb-4 py-3 px-5 border-0 fs_24 SelfStorage__bg_lightgrey',
            'placeholder': 'Ваше имя'
        })
    )
    last_name = forms.CharField(
        max_length=255,
        label='',
        widget=forms.TextInput(attrs={
            'class': 'form-control border-8 mb-4 py-3 px-5 border-0 fs_24 SelfStorage__bg_lightgrey',
            'placeholder': 'Ваше фамилия'
        })
    )
    phone = forms.CharField(
        max_length=11,
        label='',
        widget=forms.TextInput(attrs={
            'class': 'form-control border-8 mb-4 py-3 px-5 border-0 fs_24 SelfStorage__bg_lightgrey',
            'placeholder': 'Ваш телефон'
        })
    )
    password1 = forms.CharField(
        label='',
        max_length=255,
        widget=forms.PasswordInput(attrs={
            'class': 'form-control border-8 mb-4 py-3 px-5 border-0 fs_24 SelfStorage__bg_lightgrey',
            'placeholder': 'Ваш пароль'
        })
    )
    password2 = forms.CharField(
        label='',
        max_length=255,
        widget=forms.PasswordInput(attrs={
            'class': 'form-control border-8 mb-4 py-3 px-5 border-0 fs_24 SelfStorage__bg_lightgrey',
            'placeholder': 'Подтверждение пароля'
        })
    )
