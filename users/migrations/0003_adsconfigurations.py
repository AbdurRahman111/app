# Generated by Django 4.0.4 on 2022-07-31 11:42

from django.db import migrations, models
import django_cryptography.fields


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0002_delete_company'),
    ]

    operations = [
        migrations.CreateModel(
            name='AdsConfigurations',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('service_provider', models.CharField(max_length=100, verbose_name='Service Provider')),
                ('access_key', django_cryptography.fields.encrypt(models.CharField(blank=True, max_length=150, null=True, verbose_name='Access Key'))),
                ('secret_key', django_cryptography.fields.encrypt(models.CharField(blank=True, max_length=150, null=True, verbose_name='Secret Key'))),
                ('audience_id', django_cryptography.fields.encrypt(models.CharField(blank=True, max_length=150, null=True, verbose_name='Audience Id'))),
                ('app_id', django_cryptography.fields.encrypt(models.CharField(blank=True, max_length=150, null=True, verbose_name='App Id'))),
                ('developer_token', django_cryptography.fields.encrypt(models.CharField(blank=True, max_length=150, null=True, verbose_name='Developer Token'))),
                ('client_id', django_cryptography.fields.encrypt(models.CharField(blank=True, max_length=150, null=True, verbose_name='Client Id'))),
                ('client_secret', django_cryptography.fields.encrypt(models.CharField(blank=True, max_length=150, null=True, verbose_name='Client Secret'))),
                ('refresh_token', django_cryptography.fields.encrypt(models.CharField(blank=True, max_length=150, null=True, verbose_name='Refresh Token'))),
            ],
            options={
                'verbose_name_plural': 'Ads Configuration',
            },
        ),
    ]