# Generated by Django 4.2.7 on 2023-11-18 10:13

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0011_city_order_storage_city_name'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='status',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='order_status', to='main.status', verbose_name='Статус'),
        ),
        migrations.AlterField(
            model_name='order',
            name='text',
            field=models.TextField(blank=True, null=True, verbose_name='Примечание'),
        ),
    ]