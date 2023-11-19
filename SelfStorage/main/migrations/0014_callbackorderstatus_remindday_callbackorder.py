# Generated by Django 4.2.7 on 2023-11-19 06:37

from django.db import migrations, models
import django.db.models.deletion
import phonenumber_field.modelfields


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0013_order_status_remindday'),
    ]

    operations = [
        migrations.CreateModel(
            name='CallBackOrderStatus',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255)),
            ],
            options={
                'verbose_name': 'Статус заказа обратного звонка',
                'verbose_name_plural': 'Статусы заказов обратных звонков',
            },
        ),
        migrations.CreateModel(
            name='CallBackOrder',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('phone', phonenumber_field.modelfields.PhoneNumberField(max_length=128, region='RU')),
                ('first_name', models.CharField(max_length=255)),
                ('last_name', models.CharField(max_length=255)),
                ('status', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='callbackorders', to='main.callbackorderstatus')),
            ],
            options={
                'verbose_name': 'Заказ на обратный звонок',
                'verbose_name_plural': 'Заказы на обратные звонки',
            },
        ),
    ]
