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


class City(models.Model):
    name = models.CharField(
        max_length=50,
        verbose_name='Город',
        unique=True,
    )

    def __str__(self) -> str:
        return f'{self.name}'

    class Meta:
        verbose_name = 'Город'
        verbose_name_plural = 'Города'


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
    city_name = models.ForeignKey(
        City,
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        verbose_name='Город',
        related_name='storage'
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
        max_length=1000,
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

    def calc_square(self):
        return (self.length * self.weigth)/1000/10

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
    utm_source = models.CharField('Источник UTM', max_length=100, null=True, blank=True)
    utm_medium = models.CharField('Тип траффика', max_length=10, null=True, blank=True)
    utm_campaign = models.CharField('Название компании', max_length=100, null=True, blank=True)
    utm_content = models.CharField('Идентификатор объявления', max_length=250, null=True, blank=True)
    utm_term = models.CharField('Ключевое слово', max_length=100, null=True, blank=True)
    link_counter = models.IntegerField(verbose_name='Количество переходов', default=0, null=True, blank=True)

    def __str__(self) -> str:
        return f'{self.utm_source}'

    class Meta:
        verbose_name = 'UTM метка'
        verbose_name_plural = 'UTM метки'


class Order(models.Model):
    user = models.ForeignKey(
        Customer,
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        verbose_name='Пользователь',
        related_name='order_user'
    )
    box = models.ForeignKey(
        Box,
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        verbose_name='Бокс',
        related_name='order_box'
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
        related_name='order_status'
    )
    delivery = models.BooleanField(
        verbose_name='Доставка',
        blank=True,
        null=True
    )
    loaders = models.BooleanField(
        verbose_name='Грузчики',
        blank=True,
        null=True
    )
    measurement = models.BooleanField(
        verbose_name='Замерщик',
        blank=True,
        null=True
    )
    text = models.TextField(
        verbose_name='Примечание',
        blank=True,
        null=True
    )
    rise_price = models.DecimalField(
        max_digits=8,
        decimal_places=1,
        verbose_name='Цена',
        blank=True,
        null=True
    )
    def __str__(self) -> str:
        return f'{self.user.name} - {self.box.title}'

    class Meta:
        verbose_name = 'Заказ'
        verbose_name_plural = 'Заказы'


class CallBackOrder(models.Model):

    phone = PhoneNumberField(region='RU')
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    status = models.ForeignKey('CallBackOrderStatus', on_delete=models.CASCADE, related_name='callbackorders')

    def __str__(self):
        return f'{self.first_name} {self.last_name} {self.phone}'

    class Meta:
        verbose_name = 'Заказ на обратный звонок'
        verbose_name_plural = 'Заказы на обратные звонки'


class CallBackOrderStatus(models.Model):

    title = models.CharField(max_length=255)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Статус заказа обратного звонка'
        verbose_name_plural = 'Статусы заказов обратных звонков'


class RemindDay(models.Model):
    day = models.IntegerField(
        verbose_name='количество дней'
    )
    status = models.OneToOneField(
        Status,
        on_delete=models.CASCADE,
        verbose_name='статус',
        related_name='remind_day'
    )

    def __str__(self) -> str:
        return f'{self.day} - {self.status.title}'

    class Meta:
        verbose_name = 'Напоминание'
        verbose_name_plural = 'Напоминания'
