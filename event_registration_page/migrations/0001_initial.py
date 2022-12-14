# Generated by Django 4.0.4 on 2022-07-08 16:27

import ckeditor.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='app_5_website_logo',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(blank=True, max_length=255, null=True)),
                ('image', models.ImageField(upload_to='landing_page_five/logo/')),
            ],
            options={
                'verbose_name_plural': 'Website Logo (Webapp-5)',
            },
        ),
        migrations.CreateModel(
            name='Get_In_Touch_app_5',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Text', models.TextField()),
            ],
            options={
                'verbose_name_plural': 'GET IN TOUCH App-5',
            },
        ),
        migrations.CreateModel(
            name='Landing_page_five_event',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Model_event_text', ckeditor.fields.RichTextField(blank=True, null=True)),
                ('Model_event_image', models.ImageField(blank=True, null=True, upload_to='landing_page_five/event/')),
            ],
            options={
                'verbose_name_plural': 'Landing page five model event',
            },
        ),
        migrations.CreateModel(
            name='Landing_page_five_model',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Model_First_Name', models.CharField(blank=True, max_length=256, null=True)),
                ('Model_Last_Name', models.CharField(blank=True, max_length=256, null=True)),
                ('Model_Email_Address', models.CharField(blank=True, max_length=256, null=True)),
                ('Model_checked_or_not', models.CharField(blank=True, max_length=256, null=True)),
            ],
            options={
                'verbose_name_plural': 'Landing page five model',
            },
        ),
        migrations.CreateModel(
            name='Landing_page_five_model_left',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Model_left_content', ckeditor.fields.RichTextField(blank=True, null=True)),
                ('Model_full_image', models.ImageField(blank=True, null=True, upload_to='landing_page_five/full_image/')),
            ],
            options={
                'verbose_name_plural': 'Landing page five model left side',
            },
        ),
        migrations.CreateModel(
            name='social_media_app_5',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Url', models.CharField(max_length=255)),
            ],
            options={
                'verbose_name_plural': 'Social Media App-5',
            },
        ),
        migrations.CreateModel(
            name='subscribe_app_5',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('email', models.CharField(max_length=200)),
            ],
            options={
                'verbose_name_plural': 'Subscribers App-5',
            },
        ),
    ]
