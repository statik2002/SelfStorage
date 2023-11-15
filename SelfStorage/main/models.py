from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone
from phonenumber_field.modelfields import PhoneNumberField


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


class Storage(models.Model):
    title = models.CharField(
        max_length=50,
        verbose_name='Склад'
    )
    description = models.TextField(
        verbose_name='Описание'
    )
    city = models.CharField(
        max_length=50,
        verbose_name='Город'
    )
    address = models.CharField(
        max_length=200,
        verbose_name='Адрес склада'
    )
    phone = PhoneNumberField(
        verbose_name='Телефон',
        region='RU'
    )
    email = models.EmailField(
        max_length=256,
        unique=True,
        verbose_name='Email склада'
    )
    map = models.CharField(
        max_length=200,
        verbose_name='Карта'
    )
    temperature = models.DecimalField(
        max_digits=3,
        decimal_places=1,
        verbose_name='Температура на складе'
    )
    heigth = models.DecimalField(
        max_digits=3,
        decimal_places=1,
        verbose_name='Высота потолка'
    )

    def __str__(self) -> str:
        return self.title

    class Meta:
        verbose_name = 'Склад'
        verbose_name_plural = 'Склады'


class Box(models.Model):
    title = models.CharField(
        max_length=50,
        verbose_name='Бокс'
    )
    storage = models.ForeignKey(
        Storage,
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        verbose_name='Склад',
        related_name='box'
    )
    price = models.DecimalField(
        max_digits=8,
        decimal_places=1,
        verbose_name='Стоимость'
    )
    floor = models.IntegerField(
        verbose_name='Этаж'
    )
    length = models.IntegerField(
        verbose_name='Длина'
    )
    weigth = models.IntegerField(
        verbose_name='Ширина'
    )
    heigth = models.IntegerField(
        verbose_name='Высота'
    )

    def __str__(self) -> str:
        return self.title

    class Meta:
        verbose_name = 'Бокс'
        verbose_name_plural = 'Боксы'


class Status(models.Model):
    title = models.CharField(
        max_length=50,
        verbose_name='Статус'
    )

    def __str__(self) -> str:
        return self.title

    class Meta:
        verbose_name = 'Статус'
        verbose_name_plural = 'Статусы'


class Rent(models.Model):
    renter = models.ForeignKey(
        Customer,
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        verbose_name='Пользователь',
        related_name='user_rent'
    )
    box = models.ForeignKey(
        Box,
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        verbose_name='Бокс',
        related_name='box_rent'
    )
    start_date = models.DateField(
        verbose_name='Дата начала аренды'
    )
    end_date = models.DateField(
        verbose_name='Дата окончания аренды'
    )
    status = models.ForeignKey(
        Status,
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        verbose_name='Статус',
        related_name='rent'
    )

    def __str__(self) -> str:
        return f'{self.renter} - {self.box}'

    class Meta:
        verbose_name = 'Бокс в аренде'
        verbose_name_plural = 'Боксы в аренде'


class Image(models.Model):
    image = models.ImageField(
        upload_to='uploads',
        verbose_name='Картинка'
    )
    storage = models.ForeignKey(
        Storage,
        on_delete=models.CASCADE,
        verbose_name='Склад',
        related_name='image'
    )

    def __str__(self) -> str:
        return self.storage.title

    class Meta:
        verbose_name = 'Картинка'
        verbose_name_plural = 'Картинки'


class UtmMark(models.Model):
    url = models.CharField(
        max_length=200,
        verbose_name='Ссылка'
    )
    count = models.IntegerField(
        verbose_name='Количество переходов'
    )

    def __str__(self) -> str:
        return f'{self.count} - {self.url}'

    class Meta:
        verbose_name = 'Переход'
        verbose_name_plural = 'Переходы'
