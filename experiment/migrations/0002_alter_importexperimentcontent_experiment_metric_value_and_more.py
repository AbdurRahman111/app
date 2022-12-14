# Generated by Django 4.0.4 on 2022-07-12 17:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('experiment', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='importexperimentcontent',
            name='experiment_metric_value',
            field=models.FloatField(blank=True, null=True, verbose_name='Experiment Metric Value'),
        ),
        migrations.AlterField(
            model_name='importexperimentcontent',
            name='experiment_response_click',
            field=models.IntegerField(blank=True, null=True, verbose_name='Experiment Response Click'),
        ),
        migrations.AlterField(
            model_name='importexperimentcontent',
            name='experiment_response_convert',
            field=models.IntegerField(blank=True, null=True, verbose_name='Experiment Response Convert'),
        ),
        migrations.AlterField(
            model_name='importexperimentcontent',
            name='experiment_response_view',
            field=models.IntegerField(blank=True, null=True, verbose_name='Experiment Response View'),
        ),
    ]
