# Generated by Django 5.0.6 on 2024-05-25 15:42

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('trading_platform', '0003_alter_apikey_options'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='apikey',
            options={'verbose_name': 'API Key', 'verbose_name_plural': 'API Key'},
        ),
    ]