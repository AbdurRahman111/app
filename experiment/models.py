from django.db import models
from survey.utils import unique_slug_generator
from django.db.models.signals import pre_save
from datetime import datetime
from django.dispatch import receiver


File_Type = (
	('Email Template', 'Email Template'),
	('Plain Text', 'Plain Text'),
)

Experiment_Type = (
	('Created', 'Created'),
	('Imported', 'Imported'),
)

Campaign_Type = (
	('Email', 'Email'),
	('Display Ads', 'Display Ads'),
)

class Experiment(models.Model):
	experiment_name = models.CharField(max_length=250, blank=True, null=True, verbose_name='Experiment Name')
	experiment_hypothesis = models.CharField(max_length=1000, blank=True, null=True, verbose_name='Experiment Hypothesis')
	sender_email = models.CharField(max_length=50, blank=True, null=True, verbose_name='Sender Email')
	email_subject = models.CharField(max_length=150, blank=True, null=True, verbose_name='Email Subject')
	experiment_type = models.CharField(max_length=8, choices=Experiment_Type, default='Created')
	campaign_type = models.CharField(max_length=11, choices=Campaign_Type, blank=True, null=True)
	experiment_file = models.FileField(upload_to='experiments', blank=True, null=True)
	is_active = models.BooleanField(default=False)
	slug = models.SlugField(blank=True, null=True, verbose_name='Slug')

	def __str__(self):
		return f'{self.experiment_name}'
	
	def get_experiment_data(self):
		experiment_data = ImportExperimentContent.objects.filter(experiment=self)
		return experiment_data

	class Meta:
		verbose_name_plural = 'Experiments'

class ImportExperimentContent(models.Model):
	experiment = models.ForeignKey(Experiment, on_delete=models.CASCADE, related_name='experiment_import_entry', verbose_name='Experiment')
	responder_id = models.CharField(max_length=150, blank=True, null=True, verbose_name='Responder Id')
	experiment_content = models.CharField(max_length=500, blank=True, null=True, verbose_name="Experiment Content")
	response_datetime = models.DateTimeField(blank=True, null=True, verbose_name="Response Date & Time")
	experiment_launch_date = models.DateField(blank=True, null=True, verbose_name="Experiment Launch Date")
	experiment_question_type = models.CharField(max_length=250, blank=True, null=True, verbose_name="Experiment Question Type")
	experiment_response_click = models.IntegerField(blank=True, null=True, verbose_name="Experiment Response Click")
	experiment_response_view = models.IntegerField(blank=True, null=True, verbose_name="Experiment Response View")
	experiment_response_convert = models.IntegerField(blank=True, null=True, verbose_name="Experiment Response Convert")
	experiment_metric_name = models.CharField(max_length=250, blank=True, null=True, verbose_name="Experiment Metric Name")
	experiment_metric_value = models.FloatField(blank=True, null=True, verbose_name="Experiment Metric Value")
	experiment_group = models.CharField(max_length=250, blank=True, null=True, verbose_name="Experiment Group")

	def __str__(self):
		return f'Experiment # {self.experiment}, Entry # {self.id}'

	class Meta:
		verbose_name_plural = 'Imported Experiments Content'

class ExperimentGroups(models.Model):
	experiment = models.ForeignKey(Experiment, on_delete=models.CASCADE, related_name='experiment_for_group', verbose_name='Experiment')
	file_name = models.FileField(upload_to='experiment_files')
	file_type = models.CharField(max_length=40, choices=File_Type, blank=True, null=True, verbose_name='File Type')

	def __str__(self):
		return f'Experiment # {self.experiment}, Group # {self.id}'

	class Meta:
		verbose_name_plural = 'Experiments Groups'


# generates slug value according to the instance name on save, update
def slug_generator(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = unique_slug_generator(instance)

pre_save.connect(slug_generator, sender=Experiment)

# Django signals function to check if entire quantity is exchanged or not
@receiver(pre_save, sender=ImportExperimentContent)
def convertinng_date_to_datetime(instance, created, **kwargs):
	print('In pre_save')
	if created:
		response_datetime = instance.response_datetime
		launch_date = instance.launch_date

		try:
			instance.response_datetime = datetime.strptime(response_datetime, '%Y/%m/%d %H:%M')
			
		except:
			instance.response_datetime = datetime.strptime(response_datetime, '%Y-%m-%d')

		try:
			instance.launch_date = datetime.strptime(launch_date, '%Y-%m-%d')
			
		except:
			instance.launch_date = datetime.strptime(launch_date, '%Y/%m/%d')
