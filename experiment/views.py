from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from django.views.generic import View, ListView
from django.conf import settings
from django.db.models import Min, Max, Sum, Count
import csv, boto3, io
import pandas as pd
from django.contrib import messages
from datetime import datetime, date
from .models import (
	Experiment,
	ExperimentGroups,
	ImportExperimentContent,
)
from .forms import SelectExperimentForm
from survey.utils import BulkCreateManager
from surveyscaled.models import CSV
import numpy as np
from dal import autocomplete
from django.db.models.functions import ExtractWeek, ExtractYear, ExtractMonth

# Class for experiment suto complete selection field
class ExperimentAutoComplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):
        # Don't forget to filter out results depending on the visitor !
        if not self.request.user.is_authenticated:
            return Experiment.objects.none()

        qs = Experiment.objects.all()

        if self.q:
            qs = qs.filter(experiment_name__istartswith=self.q)

        return qs

class ExperimentsDashboardView(View):
	template_name = 'experiment_dashboard.html'

	def get(self, request):
		experiment_list = Experiment.objects.filter(is_active=False)
		experiment = experiment_list.last()
		experiment_data = ImportExperimentContent.objects.filter(experiment=experiment)
		if not experiment_data:
			context = {
				'title'	:	'Testscaled - Dashboard',
				'app_title'	:	'Media',
				'experiment_list'	:	experiment_list,
				'Experiment'		:	False,
				'graph_time'		:	'Week',
				'experiment_form'	:	SelectExperimentForm(request.GET),
			}
			return render(request, self.template_name, context)

		# Getting start and end date for experiment_reponse_date
		experiment_dates = experiment_data.aggregate(start_date=Min('response_datetime'), end_date=Max('response_datetime'))
		start_date = experiment_dates['start_date'].date()
		end_date = experiment_dates['end_date'].date()
		# Calculating total data entries for the experiment
		total_visits = experiment_data.count()
		# Calcultaing number of visitors for experiment
		number_of_visitors = experiment_data.values('responder_id').distinct().count()
		#Getting unique days list
		days_list = experiment_data.values_list('response_datetime').distinct()
		# Calculating number of days, for which the data is saved
		days_of_data = days_list.count()
		# Getting unique experiment_question_type for variations in analysis
		experiment_variations = experiment_data.values_list('experiment_question_type', flat=True).distinct()

		# Getting unique metric names
		experiment_metric_name = experiment_data.values_list('experiment_metric_name', flat=True).distinct()

		# Array for saving analysis data for the dashbaord table
		variations_analysis = np.array([], dtype='int16')

		# Array for saving analysis data for the dashbaord graph
		variations_analysis_graph = np.array([], dtype='int16')

		# Array for graph labels
		variations_analysis_graph_labels = []

		# Array for saving analysis data for the dashbaord graph
		variations_analysis_month_graph = np.array([], dtype='int16')

		# Array for graph labels
		variations_analysis_month_graph_labels = []

		original_conversion_rate = 0

		# Loop to create variation_analysis for the table
		for x, variation in enumerate(experiment_variations):
			# Caculating total number of visits for the variation
			experiment_variation_visits = ImportExperimentContent.objects.filter(experiment=experiment, experiment_question_type=variation).count()
			# Caculating total sum of converts for the variation
			experiment_variation_converts = ImportExperimentContent.objects.filter(experiment=experiment, experiment_question_type=variation).aggregate(Sum('experiment_response_convert'))
			# Caculating conversion rate for the variation
			experiment_variation_convertion_rate = experiment_variation_converts['experiment_response_convert__sum'] / experiment_variation_visits
			# Calculating value for variation comparison to original experiment
			if variation == 'Baseline' or variation == 'baseline':
				compare_to_original = 0
				original_conversion_rate = experiment_variation_convertion_rate
				variation_name = 'Original'

			else:
				variation_name = 'Variation ' + str(x)
				compare_to_original = ((original_conversion_rate - experiment_variation_convertion_rate)/((original_conversion_rate + experiment_variation_convertion_rate)/2)) * 100
			
			variations_analysis = np.append(
				variations_analysis,
				[
					variation_name,
					experiment_variation_visits,
					experiment_variation_converts['experiment_response_convert__sum'],
					experiment_variation_convertion_rate,
					compare_to_original,

				]
			)

			# Create experiment analysis for the graph group by week
			stats_week = (ImportExperimentContent.objects.filter(experiment=experiment, experiment_question_type=variation)
				.annotate(year=ExtractYear('response_datetime'))
				.annotate(week=ExtractWeek('response_datetime'))
				.values('year', 'week')
				.annotate(experiment_visits=Count('experiment_response_click'), conversions=Sum('experiment_response_convert'))
			)

			for data in stats_week:
				# Adding conversion rate data in graph array
				variations_analysis_graph = np.append(
					variations_analysis_graph,
					[
						data['conversions']/data['experiment_visits'],
					]
				)

				# Adding labels for graph in label array
				if x == 0:
					variations_analysis_graph_labels.append('Week '+str(data['week'])+', '+str(data['year']))

			# Create experiment analysis for the graph group by month
			stats_month = (ImportExperimentContent.objects.filter(experiment=experiment, experiment_question_type=variation)
				.annotate(year=ExtractYear('response_datetime'))
				.annotate(month=ExtractMonth('response_datetime'))
				.values('year', 'month')
				.annotate(experiment_visits=Count('experiment_response_click'), conversions=Sum('experiment_response_convert'))
			)

			for data in stats_month:
				# Adding conversion rate data in graph array
				variations_analysis_month_graph = np.append(
					variations_analysis_month_graph,
					[
						data['conversions']/data['experiment_visits'],
					]
				)

				# Adding labels for graph in label array
				if x == 0:
					import calendar
					variations_analysis_month_graph_labels.append(str(calendar.month_name[data['month']])+', '+str(data['year']))

		# Reshaping 1d to multi dimension array
		variations_analysis = np.reshape(
			variations_analysis,     # the array to be reshaped
			(len(experiment_variations),5)  # dimensions of the new array
		)

		# Reshaping 1d to multi dimension array
		variations_analysis_graph = np.reshape(
			variations_analysis_graph,     # the array to be reshaped
			(len(experiment_variations),len(variations_analysis_graph_labels))  # dimensions of the new array
		)

		# Reshaping 1d to multi dimension array
		variations_analysis_month_graph = np.reshape(
			variations_analysis_month_graph,     # the array to be reshaped
			(len(experiment_variations),len(variations_analysis_month_graph_labels))  # dimensions of the new array
		)

		context = {
			'title'	:	'Testscaled - Dashboard',
			'app_title'	:	'Media',
			'experiment_list'	:	experiment_list,
			'total_visits'		:	total_visits,
			'days_of_data'		:	days_of_data,
			'number_of_visitors':	number_of_visitors,
			'experiment_variations'	:	experiment_variations,
			'variations_analysis'	:	variations_analysis,
			'original_conversion_rate'	:	original_conversion_rate,
			'variations_analysis_graph'	:	variations_analysis_graph,
			'variations_analysis_graph_labels'	:	variations_analysis_graph_labels,
			'variations_analysis_month_graph'	:	variations_analysis_month_graph,
			'variations_analysis_month_graph_labels'	:	variations_analysis_month_graph_labels,
			'graph_time'		:	'Week',
			'experiment_metric_name'	:	experiment_metric_name,
			'Experiment'		:	True,
			'experiment_form'	:	SelectExperimentForm(request.GET),
		}
		return render(request, self.template_name, context)

	def post(self, request):
		experiment_list = Experiment.objects.filter(is_active=False)
		experiment_query = request.POST.get('experiment_name', None)
		# Checking if query exists or not
		if experiment_query:
			try:
				experiment = experiment_list.get(pk=experiment_query)
				experiment_data = ImportExperimentContent.objects.filter(experiment=experiment)

			except Exception as exc:
				context = {
					'title'	:	'Testscaled - Dashboard',
					'app_title'	:	'Media',
					'experiment_list'	:	experiment_list,
					'Experiment'		:	False,
					'graph_time'		:	'Week',
					'experiment_form'	:	SelectExperimentForm(request.GET),
				}
				return render(request, self.template_name, context)

			# Getting start and end date for experiment_reponse_date
			experiment_dates = experiment_data.aggregate(start_date=Min('response_datetime'), end_date=Max('response_datetime'))
			start_date = experiment_dates['start_date'].date()
			end_date = experiment_dates['end_date'].date()
			# Calculating total data entries for the experiment
			total_visits = experiment_data.count()
			# Calcultaing number of visitors for experiment
			number_of_visitors = experiment_data.values('responder_id').distinct().count()
			#Getting unique days list
			days_list = experiment_data.values_list('response_datetime').distinct()
			# Calculating number of days, for which the data is saved
			days_of_data = days_list.count()
			# Getting unique experiment_question_type for variations in analysis
			experiment_variations = experiment_data.values_list('experiment_question_type', flat=True).distinct()

			if experiment_variations:

				# Array for saving analysis data for the dashbaord table
				variations_analysis = np.array([], dtype='int16')

				# Array for saving analysis data for the dashbaord graph
				variations_analysis_graph = np.array([], dtype='int16')

				# Array for graph labels
				variations_analysis_graph_labels = []

				# Array for saving analysis data for the dashbaord graph
				variations_analysis_month_graph = np.array([], dtype='int16')

				# Array for graph labels
				variations_analysis_month_graph_labels = []

				original_conversion_rate = 0

				# Loop to create variation_analysis for the table
				for x, variation in enumerate(experiment_variations):
					# Caculating total number of visits for the variation
					experiment_variation_visits = ImportExperimentContent.objects.filter(experiment=experiment, experiment_question_type=variation).count()
					# Caculating total sum of converts for the variation
					experiment_variation_converts = ImportExperimentContent.objects.filter(experiment=experiment, experiment_question_type=variation).aggregate(Sum('experiment_response_convert'))
					# Caculating conversion rate for the variation
					experiment_variation_convertion_rate = experiment_variation_converts['experiment_response_convert__sum'] / experiment_variation_visits
					# Calculating value for variation comparison to original experiment
					if variation == 'Baseline' or variation == 'baseline':
						compare_to_original = 0
						original_conversion_rate = experiment_variation_convertion_rate
						variation_name = 'Original'

					else:
						variation_name = 'Variation ' + str(x)
						compare_to_original = ((original_conversion_rate - experiment_variation_convertion_rate)/((original_conversion_rate + experiment_variation_convertion_rate)/2)) * 100
					
					variations_analysis = np.append(
						variations_analysis,
						[
							variation_name,
							experiment_variation_visits,
							experiment_variation_converts['experiment_response_convert__sum'],
							experiment_variation_convertion_rate,
							compare_to_original,

						]
					)

					# Create experiment analysis for the graph group by week
					stats_week = (ImportExperimentContent.objects.filter(experiment=experiment, experiment_question_type=variation)
						.annotate(year=ExtractYear('response_datetime'))
						.annotate(week=ExtractWeek('response_datetime'))
						.values('year', 'week')
						.annotate(experiment_visits=Count('experiment_response_click'), conversions=Sum('experiment_response_convert'))
					)

					for data in stats_week:
						# Adding conversion rate data in graph array
						variations_analysis_graph = np.append(
							variations_analysis_graph,
							[
								data['conversions']/data['experiment_visits'],
							]
						)

						# Adding labels for graph in label array
						if x == 0:
							variations_analysis_graph_labels.append('Week '+str(data['week'])+', '+str(data['year']))

					# Create experiment analysis for the graph group by month
					stats_month = (ImportExperimentContent.objects.filter(experiment=experiment, experiment_question_type=variation)
						.annotate(year=ExtractYear('response_datetime'))
						.annotate(month=ExtractMonth('response_datetime'))
						.values('year', 'month')
						.annotate(experiment_visits=Count('experiment_response_click'), conversions=Sum('experiment_response_convert'))
					)

					for data in stats_month:
						# Adding conversion rate data in graph array
						variations_analysis_month_graph = np.append(
							variations_analysis_month_graph,
							[
								data['conversions']/data['experiment_visits'],
							]
						)

						# Adding labels for graph in label array
						if x == 0:
							import calendar
							variations_analysis_month_graph_labels.append(str(calendar.month_name[data['month']])+', '+str(data['year']))

				# Reshaping 1d to multi dimension array
				variations_analysis = np.reshape(
					variations_analysis,     # the array to be reshaped
					(len(experiment_variations),5)  # dimensions of the new array
				)

				# Reshaping 1d to multi dimension array
				variations_analysis_graph = np.reshape(
					variations_analysis_graph,     # the array to be reshaped
					(len(experiment_variations),len(variations_analysis_graph_labels))  # dimensions of the new array
				)

				# Reshaping 1d to multi dimension array
				variations_analysis_month_graph = np.reshape(
					variations_analysis_month_graph,     # the array to be reshaped
					(len(experiment_variations),len(variations_analysis_month_graph_labels))  # dimensions of the new array
				)

				context = {
					'title'	:	'Testscaled - Dashboard',
					'app_title'	:	'Media',
					'experiment_list'	:	experiment_list,
					'total_visits'		:	total_visits,
					'days_of_data'		:	days_of_data,
					'number_of_visitors':	number_of_visitors,
					'experiment_variations'	:	experiment_variations,
					'variations_analysis'	:	variations_analysis,
					'original_conversion_rate'	:	original_conversion_rate,
					'variations_analysis_graph'	:	variations_analysis_graph,
					'variations_analysis_graph_labels'	:	variations_analysis_graph_labels,
					'variations_analysis_month_graph'	:	variations_analysis_month_graph,
					'variations_analysis_month_graph_labels'	:	variations_analysis_month_graph_labels,
					'graph_time'		:	'Week',
					'Experiment'		:	True,
					'experiment_form'	:	SelectExperimentForm(request.GET),
				}
				return render(request, self.template_name, context)

			else:
				messages.error(request, 'Looks like an error occured. Please try again')
				return redirect('experiment:experiment-dashboard')
		else:
			messages.error(request, "Experiment doesn't exist in the database")
			return redirect('experiment:experiment-dashboard')
 
class UploadClosedExperimentView(View):
	template_name = 'upload_experiment.html'

	def get(self, request):
		context = {
			'title'	:	'Testscaled - Upload Closed Experiment',
		}
		return render(request, self.template_name, context)

	def post(self, request):
		file = request.FILES['experiment-file']
		experiment_name = request.POST.get('experiment-name')
		experiment_obj = Experiment(experiment_name=experiment_name, experiment_file=file, experiment_type='Imported')
		experiment_obj.save()

		if settings.DEBUG:
			# Reading file from media files in django
			df = pd.read_csv(experiment_obj.experiment_file, sep=',')

		else:
			# Reading file saved in AWS S3 Bucket
			FORECAST_DATA_OBJECT = experiment_obj.experiment_file.name
			s3 = boto3.client(
			    's3',
			    aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
			    aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
			)
			try:
				obj = s3.get_object(Bucket=settings.AWS_STORAGE_BUCKET_NAME, Key=FORECAST_DATA_OBJECT)

			except Exception as exc:
				return JsonResponse({"success": False, 'aws': True, "message": "Error! AWS not responding please try again"}, safe=False)

			data = obj['Body'].read().decode('utf-8')

			# Saving csv file data with pandas
			df=pd.read_csv(io.StringIO(data), sep=',')

		# Checking if file has correct columns in it
		if 'responder_id' in df.columns and 'experiment_content' in df.columns and 'response_datetime' in df.columns and 'experiment_launch_date' in df.columns and 'experiment_question_type' in df.columns and 'experiment_response_click' in df.columns and 'experiment_response_view' in df.columns and 'experiment_response_convert' in df.columns and 'experiment_metric_name' in df.columns and 'experiment_metric_value' in df.columns and 'experiment_group' in df.columns :
			row_iter = df.iterrows()
			bulk_mgr = BulkCreateManager(chunk_size=100)
			for index, row in row_iter:
				try:
					response_datetime = datetime.strptime(row['response_datetime'], '%Y-%m-%d %H:%M')
					
				except:
					try:
						response_datetime = datetime.strptime(row['response_datetime'], '%Y-%m-%d')

					except:
						response_datetime = datetime.strptime(row['response_datetime'], '%d-%m-%Y')
				try:
					experiment_launch_date = datetime.strptime(row['experiment_launch_date'], '%Y-%m-%d')
					
				except:
					try:
						experiment_launch_date = datetime.strptime(row['experiment_launch_date'], '%Y/%m/%d')

					except:
						experiment_launch_date = datetime.strptime(row['experiment_launch_date'], '%d-%m-%Y')

				bulk_mgr.add(
					ImportExperimentContent(experiment=experiment_obj, 
					responder_id = row['responder_id'],
					experiment_content  = row['experiment_content'],
					response_datetime  = response_datetime,
					experiment_launch_date  = experiment_launch_date,
					experiment_question_type = row['experiment_question_type'],
					experiment_response_click  = row['experiment_response_click'],
					experiment_response_view  = row['experiment_response_view'],
					experiment_response_convert  = row['experiment_response_convert'],
					experiment_metric_name  = row['experiment_metric_name'],
					experiment_metric_value  = row['experiment_metric_value'],
					experiment_group  = row['experiment_group'])
				)
			bulk_mgr.done()
			messages.success(request, 'Experiment response uploaded successfuly')
			return JsonResponse({"success": True, "message": "Data saved successfuly"}, safe=False)

		else:
			print('Not same')
			experiment_obj.delete()
			return JsonResponse({"success": False, "message": "File format is not correct"}, safe=False)

class CreateEmailExperimentView(View):
	template_name = 'create_experiment.html'

	def get(self, request):
		context = {
			'title'	:	'Create Email Experiment',
			'type'	:	'Email',
			'heading'	:	'Upload Email Content',
		}
		return render(request, self.template_name, context)

	def post(self, request):
		total_forms = int(request.POST.get('experiment_form-TOTAL_FORMS'))
		experiment_name = request.POST.get('experiment-name')
		experiment_hypothesis = request.POST.get('experiment-hypothesis')
		experiment_sender_email	= request.POST.get('sender-email')
		experiment_sender_email_subject = request.POST.get('sender-email-subject')
		experiment_obj = Experiment(experiment_name=experiment_name, campaign_type='Email', experiment_type='Created', experiment_hypothesis=experiment_hypothesis, sender_email=experiment_sender_email, email_subject=experiment_sender_email_subject, is_active=True)
		experiment_obj.save()
		# Fetching data for each group
		for x in range(total_forms):
			email_file = request.FILES.get('id_form-'+str(x)+'-email-experiment-template-file', None)
			file_type = request.POST.get('id_form-'+str(x)+'-email-experiment-upload-file-type', None)
			groups_obj = ExperimentGroups(file_name=email_file, file_type=file_type, experiment=experiment_obj)
			groups_obj.save()

		messages.success(request, 'Email campaign registered successfuly')
		return redirect('experiment:experiment-dashboard')

class CreateDisplayExperimentView(View):
	template_name = 'create_experiment.html'

	def get(self, request):
		context = {
			'title'	:	'Create Display Experiment',
			'type'	:	'Display',
			'heading'	:	'Upload Display for Experiment',
		}
		return render(request, self.template_name, context)

	def post(self, request):
		total_forms = int(request.POST.get('experiment_form-TOTAL_FORMS'))
		experiment_name = request.POST.get('experiment-name')
		experiment_hypothesis = request.POST.get('experiment-hypothesis')
		experiment_obj = Experiment(experiment_name=experiment_name, experiment_hypothesis=experiment_hypothesis, campaign_type='Display Ads', experiment_type='Created', is_active=True)
		experiment_obj.save()
		# Fetching data for each group
		for x in range(total_forms):
			email_file = request.FILES.get('id_form-'+str(x)+'-email-experiment-template-file', None)
			file_type = request.POST.get('id_form-'+str(x)+'-email-experiment-upload-file-type', None)
			groups_obj = ExperimentGroups(file_name=email_file, file_type=file_type, experiment=experiment_obj)
			groups_obj.save()

		messages.success(request, 'display ad campaign registered successfuly')
		return redirect('experiment:experiment-dashboard')

def FileRenderingVidew(request):
	file  = request.GET.get('file_path')
	if file:
		filehandle = open(file)
		filehandle.close()

	return JsonResponse({"success": True})

class ExperimentListView(View):
	template_name = 'experiment_list.html'

	def get(self, request):
		experiment_list = Experiment.objects.all()
		context = {
			'title'	:	'Testscaled - Experiment List',
			'object_list'	:	experiment_list,
			'list_experiments'	:	experiment_list.filter(experiment_type='Created'),
			'experiment_form'	:	SelectExperimentForm(request.GET),
		}
		return render(request, self.template_name, context)

# View for executing email experiment
class ExecuteEmailExperimentView(View):

	def get(self, request):
		pass

	def post(self, request):
		campaign_start_date = request.POST.get("campaign-start-date", None)
		campaign_end_date = request.POST.get("campaign-end-date", None)
		campaign_frequency = request.POST.get("campaign-frequency", None)
		campaign_email_list = request.FILES.get("campaign-email-list", None)
		campaign_name = request.POST.get("campaign-name", None)
		campaing_test_percentage = request.POST.get("campaign-test-percentage", None)
		campaign_control_percentage = request.POST.get("campaign-control-percentage", None)
		save_email_list = request.POST.get("save-email-list", None)
		email_file = request.FILES.get('email-file', None)