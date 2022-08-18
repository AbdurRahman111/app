# Generated by Django 4.0.4 on 2022-07-08 15:17

import ckeditor.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='app_1_website_logo',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(blank=True, max_length=255, null=True)),
                ('image', models.ImageField(upload_to='landing_page_one/logo/')),
            ],
            options={
                'verbose_name_plural': 'Website Logo (Webapp-1)',
            },
        ),
        migrations.CreateModel(
            name='Get_In_Touch_app1',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Text', models.TextField()),
            ],
            options={
                'verbose_name_plural': 'GET IN TOUCH App-1',
            },
        ),
        migrations.CreateModel(
            name='Landing_page_one_model',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Mobel_First_Name', models.CharField(blank=True, max_length=256, null=True)),
                ('Mobel_Last_Name', models.CharField(blank=True, max_length=256, null=True)),
                ('Mobel_Email_Address', models.CharField(blank=True, max_length=256, null=True)),
                ('Mobel_Date_of_Birth', models.DateField(blank=True, max_length=256, null=True)),
                ('Mobel_City', models.CharField(blank=True, max_length=256, null=True)),
                ('Mobel_State', models.CharField(blank=True, max_length=256, null=True)),
                ('Mobel_Zip_Code', models.CharField(blank=True, max_length=256, null=True)),
                ('Model_checked_or_not', models.CharField(blank=True, max_length=256, null=True)),
            ],
            options={
                'verbose_name_plural': 'Landing page one model',
            },
        ),
        migrations.CreateModel(
            name='Landing_page_one_model_left',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Mobel_left_content', ckeditor.fields.RichTextField(blank=True, null=True)),
                ('Mobel_left_image', models.ImageField(blank=True, null=True, upload_to='landing_page_one/left_image/')),
            ],
            options={
                'verbose_name_plural': 'Landing page one model left side',
            },
        ),
        migrations.CreateModel(
            name='social_media_app1',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Url', models.CharField(max_length=255)),
            ],
            options={
                'verbose_name_plural': 'Social Media App-1',
            },
        ),
        migrations.CreateModel(
            name='subscribe_app1',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('email', models.CharField(max_length=200)),
            ],
            options={
                'verbose_name_plural': 'Subscribers App-1',
            },
        ),
    ]
