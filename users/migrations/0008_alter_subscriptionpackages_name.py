# Generated by Django 4.0.4 on 2022-07-31 21:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0007_subscriptionsdetails_subscription_plan'),
    ]

    operations = [
        migrations.AlterField(
            model_name='subscriptionpackages',
            name='name',
            field=models.CharField(max_length=150, unique=True),
        ),
    ]
