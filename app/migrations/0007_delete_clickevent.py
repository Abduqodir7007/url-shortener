# Generated by Django 5.2 on 2025-05-06 13:41

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0006_alter_url_short_url'),
    ]

    operations = [
        migrations.DeleteModel(
            name='ClickEvent',
        ),
    ]
