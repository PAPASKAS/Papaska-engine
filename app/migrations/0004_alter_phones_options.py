# Generated by Django 4.1 on 2022-08-25 12:49

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0003_alter_phones_before_discount'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='phones',
            options={'ordering': ['shop', 'name']},
        ),
    ]
