# Generated by Django 4.1.1 on 2022-09-12 17:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('records', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='increaserecord',
            name='checked',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='salerecord',
            name='checked',
            field=models.BooleanField(default=False),
        ),
    ]