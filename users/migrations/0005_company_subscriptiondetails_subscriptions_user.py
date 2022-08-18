# Generated by Django 4.0.4 on 2022-07-31 19:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0004_rename_subscriptiondetails_subscriptionsdetails'),
    ]

    operations = [
        migrations.CreateModel(
            name='Company',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('company_id', models.CharField(max_length=150, unique=True)),
                ('company_name', models.CharField(max_length=150, unique=True)),
                ('group', models.CharField(max_length=150)),
                ('company_address', models.CharField(max_length=250)),
                ('city', models.CharField(max_length=150)),
                ('zip_code', models.CharField(max_length=150)),
                ('country', models.CharField(max_length=150)),
                ('state', models.CharField(max_length=150)),
                ('company_phone', models.CharField(max_length=150)),
                ('company_email', models.CharField(max_length=150)),
                ('contact_name', models.CharField(max_length=150)),
                ('contact_email', models.CharField(max_length=150)),
                ('contact_phone', models.CharField(max_length=150)),
                ('date', models.DateField()),
            ],
            options={
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='SubscriptionDetails',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('subscription_id', models.CharField(blank=True, max_length=25, null=True)),
                ('stripeid', models.CharField(blank=True, max_length=150, null=True)),
                ('payment', models.CharField(blank=True, max_length=150, null=True)),
                ('status', models.CharField(blank=True, max_length=150, null=True)),
            ],
            options={
                'db_table': 'subscription_details',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='Subscriptions',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('subscription_id', models.CharField(blank=True, max_length=25, null=True)),
                ('subscription_plan', models.CharField(max_length=150)),
                ('subscription_type', models.CharField(max_length=150)),
                ('subscription_name', models.CharField(max_length=150)),
                ('product_group_count', models.IntegerField()),
                ('ncountry', models.IntegerField()),
                ('store_category_count', models.IntegerField()),
                ('n_users', models.IntegerField()),
                ('n_data_loads', models.IntegerField()),
                ('status', models.CharField(max_length=50)),
                ('start_date', models.DateField()),
                ('end_date', models.DateField()),
                ('setup_price', models.FloatField()),
                ('base_monthly_unit_price', models.FloatField()),
                ('base_monthly_unit_discount', models.FloatField()),
                ('contracted_installments', models.IntegerField()),
                ('max_number_of_markets', models.IntegerField()),
                ('max_installments', models.IntegerField()),
                ('total_monthly_amount', models.FloatField()),
                ('create_date', models.DateField()),
            ],
            options={
                'db_table': 'subscriptions',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('username', models.CharField(blank=True, max_length=150, null=True, unique=True)),
                ('email', models.CharField(blank=True, max_length=150, null=True, unique=True)),
                ('password', models.BinaryField(blank=True, null=True)),
                ('authenticated', models.BooleanField(blank=True, null=True)),
                ('email_confirmation_sent_on', models.DateTimeField(blank=True, null=True)),
                ('email_confirmed', models.BooleanField(blank=True, null=True)),
                ('email_confirmed_on', models.DateTimeField(blank=True, null=True)),
            ],
            options={
                'db_table': 'User',
                'managed': False,
            },
        ),
    ]
