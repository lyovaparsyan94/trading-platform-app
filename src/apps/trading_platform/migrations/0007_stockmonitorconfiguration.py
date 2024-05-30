# Generated by Django 5.0.6 on 2024-05-30 12:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('trading_platform', '0006_remove_indicatorsetting_indicator_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='StockMonitorConfiguration',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('email', models.EmailField(max_length=254, verbose_name='Email')),
                ('password', models.CharField(max_length=255, verbose_name='Password')),
            ],
            options={
                'verbose_name': 'Stock Monitor Configuration',
                'verbose_name_plural': 'Stock Monitor Configuration',
            },
        ),
    ]
