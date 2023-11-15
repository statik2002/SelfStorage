from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone


class CustomerManager(BaseUserManager):
    def create_user(self, name, email, password=None, **extra_fields):
        if not name:
            raise ValueError('Необходимо указать имя')
        if not email:
            raise ValueError('Необходимо указать адрес электронной почты')
        user = self.model(name=name, email=email, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, name, email,  password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)
        return self.create_user(name, email, password, **extra_fields)


class Customer(AbstractUser):
    username = None
    email = models.EmailField(max_length=256, unique=True)
    first_name = models.CharField(max_length=256, null=True, blank=True)
    last_name = models.CharField(max_length=256, null=True, blank=True)
    is_read_pd = models.BooleanField(default=False)
    name = models.CharField(
        'Имя пользователя',
        max_length=100,
        default='',
        blank=True,
    )
    phone_number = models.CharField(
        'Номер телефона',
        max_length=20,
        unique=True,
    )
    date_joined = models.DateTimeField(
        'Дата регистрации',
        default=timezone.now
    )
    avatar = models.ImageField(blank=True, null=True, upload_to='avatars/')

    REQUIRED_FIELDS = ['name']
    USERNAME_FIELD = 'email'

    objects = CustomerManager()

    def __str__(self) -> str:
        return self.name

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'
