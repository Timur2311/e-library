# Generated by Django 4.0.4 on 2022-06-12 14:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0004_contactus'),
    ]

    operations = [
        migrations.AlterField(
            model_name='feedback',
            name='text',
            field=models.TextField(blank=True, max_length=1000, null=True, verbose_name='Сообщение'),
        ),
    ]