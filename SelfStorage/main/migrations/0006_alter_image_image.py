# Generated by Django 4.2.7 on 2023-11-15 10:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0005_box_status_storage_utmmark_rent_image_box_storage'),
    ]

    operations = [
        migrations.AlterField(
            model_name='image',
            name='image',
            field=models.ImageField(upload_to='uploads', verbose_name='Картинка'),
        ),
    ]
