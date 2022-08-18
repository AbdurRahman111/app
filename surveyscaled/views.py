from django.shortcuts import render, redirect
from django.views.generic import View, ListView
# import json
# from json import JSONEncoder
# from django.core import serializers
from django.http import HttpResponse, JsonResponse
from django.contrib.sites.models import Site
from django.views.generic import View, ListView
from django.template.loader import get_template
from django.core.mail import EmailMessage
from django.conf import settings
from django.contrib import messages
from pathlib import Path
from django.db.models import Count
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from datetime import datetime, timedelta
import csv, io, boto3 
from survey.utils import BulkCreateManager
import numpy as np
import pandas as pd
# Imports for mailchimp marketing api
from mailchimp_marketing import Client
from mailchimp_marketing.api_client import ApiClientError
from users.models import SubscriptionsDetails
from .models import (
	CompanyEmailDetails,
	UserDetails,
	Survey,
	SurveyQuestions,
	SurveyQuestionAnswers,
	SurveyAnswers,
	CSV,
	Survey_Metas,
	Survey_Metas_Questions,
	Survey_Metas_Answers,
)
from .forms import (
	UserDetailsForm,
	SurveyForm,
	SurveyQuestionsForm,
	SurveyQuestionsFormset,
)
from survey import mailchimp_marketing_api

# Function to handle to email sending using mailchimp marketing api for survey response invites
def send_survey_invite_email(email):
	"""
	 Contains code handling the communication to the mailchimp api
	 to create a contact/member in an audience/list.
	"""

	mailchimp = Client()
	mailchimp.set_config({
		"api_key": settings.MAILCHIMP_API_KEY,
		"server": settings.MAILCHIMP_DATA_CENTER,
	})

	member_info = {
		"email_address": email,
		"status": "subscribed",
	}

	try:
		response = mailchimp.lists.add_list_member(settings.MAILCHIMP_EMAIL_LIST_ID, member_info)
		print("response: {}".format(response))
	except ApiClientError as error:
		print("An exception occurred: {}".format(error.text))

# Suverscaled dashbaord view. Only surveys created through this app are displayed on dashbaord
class SurveyDashboardView(View):
	template_name = 'survey_dashboard.html'
	
	def get(self, request):
		survey_obj = Survey.objects.all()
		today = datetime.today()
		first = today.replace(day=1)  # first date of current month
		previous_month_date = first - timedelta(days=1)  # this will be the last day of previous month
		# Getting surveys created last month
		previous_month_surveys_obj = survey_obj.filter(created_on__month=previous_month_date.month, created_on__year=previous_month_date.year)
		# Getting surveys created this month
		this_month_surveys_obj = survey_obj.filter(created_on__month=today.month, created_on__year=today.year)
		
		if previous_month_surveys_obj.count():
			# Calculation month over month growth for survey creation
			growth_over_previous_month = (this_month_surveys_obj.count() - previous_month_surveys_obj.count()) * (100 / previous_month_surveys_obj.count())
		else:
			growth_over_previous_month = 100


		# Getting active surrvey details
		active_surveys = survey_obj.filter(is_active=True).count()

		#Paginating survey list
		page = request.GET.get('page', 1)
		paginator = Paginator(survey_obj, 2)
		try:
			survey_list = paginator.page(page)
		except PageNotAnInteger:
			survey_list = paginator.page(1)
		except EmptyPage:
			survey_list = paginator.page(paginator.num_pages)


		# getting latest survey
		try:
			survey = survey_obj[0]

		except Exception as exc:
			print('Exception error: ',exc)
			context = {
				'title'	:	'Surveyscaled - Dashboard',
				'survey_obj'	:	survey_obj,
				'previous_month_surveys_obj'	:	previous_month_surveys_obj,
				'growth_over_previous_month'	:	growth_over_previous_month,
				'new_survey_count'	:	this_month_surveys_obj.count(),
				'active_surveys'	:	active_surveys,
				'survey_list'	:	survey_list,
			}
			return render(request, self.template_name, context)

		context = {
			'title'	:	'Surveyscaled - Dashboard',
			'survey_obj'	:	survey_obj,
			'previous_month_surveys_obj'	:	previous_month_surveys_obj,
			'growth_over_previous_month'	:	growth_over_previous_month,
			'new_survey_count'	:	this_month_surveys_obj.count(),
			'active_surveys'	:	active_surveys,
			'survey'		:	survey,
			'survey_list'	:	survey_list,
		}
		return render(request, self.template_name, context)

# View to load choosen surveys analysis on dashboard
def SurveyResponseAPIView(request, pk):	
	survey_obj = Survey.objects.all()
	today = datetime.today()
	first = today.replace(day=1)  # first date of current month
	previous_month_date = first - timedelta(days=1)  # this will be the last day of previous month
	# Getting surveys created last month
	previous_month_surveys_obj = survey_obj.filter(created_on__month=previous_month_date.month, created_on__year=previous_month_date.year)
	# Getting surveys created this month
	this_month_surveys_obj = survey_obj.filter(created_on__month=today.month, created_on__year=today.year)
	
	if previous_month_surveys_obj.count():
		# Calculation month over month growth for survey creation
		growth_over_previous_month = (this_month_surveys_obj.count() - previous_month_surveys_obj.count()) * (100 / previous_month_surveys_obj.count())
	else:
		growth_over_previous_month = 100

	# Getting active surrvey details
	active_surveys = survey_obj.filter(is_active=True).count()

	# getting latest survey
	survey = Survey.objects.get(survey_no=pk)
	
	#Paginating survey list
	page = request.GET.get('page', 1)
	paginator = Paginator(survey_obj, 2)
	try:
		survey_list = paginator.page(page)
	except PageNotAnInteger:
		survey_list = paginator.page(1)
	except EmptyPage:
		survey_list = paginator.page(paginator.num_pages)

	context = {
		'title'	:	'Surveyscaled - Dashboard',
		'survey_obj'	:	survey_obj,
		'previous_month_surveys_obj'	:	previous_month_surveys_obj,
		'growth_over_previous_month'	:	growth_over_previous_month,
		'new_survey_count'	:	this_month_surveys_obj.count(),
		'active_surveys'	:	active_surveys,
		'survey'		:	survey,
		'survey_list'	:	survey_list,
	}
	return render(request, 'survey_dashboard.html', context)

# class NumpyArrayEncoder(JSONEncoder):
#     def default(self, obj):
#         if isinstance(obj, np.ndarray):
#             return obj.tolist()
#         return JSONEncoder.default(self, obj)

# View to create surveys
class CreateSurveyView(View):
	template_name = 'create_survey.html'
	form_class = SurveyForm
	formset_class = SurveyQuestionsFormset

	def get(self, request):
		context = {
			'page_title'	:	'Create New Survey',
		}
		return render(request, self.template_name, context)

	def post(self, request):
		survey_name = request.POST.get('survey_name', None)
		survey_purpose = request.POST.get('survey_purpose', None)
		# Getting current logged in user
		current_user = request.user
		try:
			subscription_obj = SubscriptionsDetails.objects.get(user=current_user)

		except Exception as exc:
			print('Error! ',exc)
			context = {
				'page_title'	:	'Create New Survey',
			}
			messages.error(request, 'Opps! You are not linked with any company subscription. Please contact admin support for further information')
			return render(request, self.template_name, context)

		if survey_name:
			try:
				survey_obj = Survey(name=survey_name, 
					survey_purpose=survey_purpose, 
					company_id=subscription_obj.company_id, 
					subscription_id=subscription_obj.subscription_id,
					created_by = current_user
				)
				survey_obj.save()

			except Exception as exc:
				print('Error! ',exc)
				context = {
					'page_title'	:	'Create New Survey',
				}
				messages.error(request, 'Opps! Sorry looks like we faced an error while creating your survey. Please contact admin support for further information')
				return render(request, self.template_name, context)

			total_number_of_forms = int(request.POST.get('form-TOTAL_FORMS'))
			# Fetching all the questions and saving them in database
			for count in range(total_number_of_forms):
				question_number = request.POST.get('form-' + str(count) + '-question_no')
				question_statement = request.POST.get('form-' + str(count) + '-question_statement')
				question_type = request.POST.get('form-' + str(count) + '-question_type')

				try:
					# Saving questions for survey
					question_obj = SurveyQuestions(survey_no=survey_obj,
						question_no = question_number,
						question_statement = question_statement,
						question_type = question_type,
					)
					question_obj.save()

				except Exception as exc:
					print('Error! ',exc)
					# Deleting survey
					survey_obj.delete()
					context = {
						'page_title'	:	'Create New Survey',
					}
					messages.error(request, 'Opps! Sorry looks like we faced an error while creating your survey. Please contact admin support for further information')
					return render(request, self.template_name, context)

				# Checking if question type is scaled question to get scale type of the question
				if question_type == 'Scaled Question':
					scale_type = request.POST.get('form-' + str(count) + '-scaled_question_scale')
					question_obj.scale_type = scale_type
					question_obj.save()

				# Checking if question type is multiple choices question to get answers for the question
				if question_type == 'Multiple Choices - Select One Answer' or question_type == 'Multiple Choices - Select All That Applies':
					number_of_answers = int(request.POST.get('form-' + str(count) + '-number_of_answers'))
					question_obj.number_of_answers = number_of_answers
					question_obj.save()

					for counter in range(number_of_answers):
						answer_statement = request.POST.get('form-' + str(count) + '-questions_answer_' + str(counter))
						try:
							# Saving answers for multiple chioces questions
							answers_obj = SurveyQuestionAnswers(survey_no=survey_obj,
								question_no = question_obj,
								answer_statement = answer_statement,
							)
							answers_obj.save()

						except Exception as exc:
							print('Error! ',exc)
							# Deleting survey
							survey_obj.delete()
							context = {
								'page_title'	:	'Create New Survey',
							}
							messages.error(request, 'Opps! Sorry looks like we faced an error while creating your survey. Please contact admin support for further information')
							return render(request, self.template_name, context)

			messages.success(request, 'Survey created')
			return redirect('surveyscaled:survey-created', survey_obj.slug)

		else:
			context = {
				'page_title'	:	'Create New Survey',
			}
			messages.error(request, 'Please provide survey name. Make sure all fields are filed with respective information')
			return render(request, self.template_name, context)

# View to display user created surveys list
class SurveyListView(ListView):
    model = Survey
    paginate_by = 15
    context_object_name = 'surveys'
    template_name = 'survey_list.html'
    ordering = ['-survey_no']

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = 'Surveyscaled - Survey List'
        context["page"] = 'survey'
        return context

# View for editing user created surveys
class EditSurveyView(View):
	template_name = 'edit_survey.html'

	def get(self, request, slug):
		try:
			survey_obj = Survey.objects.get(slug=slug)
		except Exception as exc:
			print('Exception error: ',exc)
			messages.error(request, 'Could not found requested survey')
			return redirect('surveyscaled:create-survey')

		survey_questions = SurveyQuestions.objects.filter(survey_no=survey_obj)
		context = {
			'survey_obj'	:	survey_obj,
			'survey_questions'	:	survey_questions,
			'page_title'	:	'Send Survey Email',
		}
		return render(request, self.template_name, context)

	def post(self, request, slug):
		try:
			survey_obj = Survey.objects.get(slug=slug)
			survey_questions = SurveyQuestions.objects.filter(survey_no=survey_obj)

		except Exception as exc:
			print('Exception error: ',exc)
			messages.error(request, 'Could not found requested survey')
			return redirect('surveyscaled:create-survey')

		try:
			survey_obj.survey_name = request.POST.get('survey_name')
			survey_obj.survey_purpose = request.POST.get('survey_purpose')
			survey_obj.save()

		except Exception as exc:
			print('Error! ',exc)
			context = {
				'survey_obj'	:	survey_obj,
				'survey_questions'	:	survey_questions,
				'page_title'	:	'Send Survey Email',
			}
			messages.error(request, 'Opps! Sorry looks like we faced an error while updating your survey. Please contact admin support for further information')
			return render(request, self.template_name, context)

		for question in survey_questions:
			try:
				question.question_statement = request.POST.get('question-'+str(question.question_no)+'-statement')
				question.question_no = request.POST.get('question-number-'+str(question.question_no))
				question.question_type = request.POST.get('question-'+str(question.question_no)+'-question_type')
				question.scale_type = request.POST.get('question-'+str(question.question_no)+'-scale_type')
				question.save()

			except Exception as exc:
				print('Error! ',exc)
				context = {
					'survey_obj'	:	survey_obj,
					'survey_questions'	:	survey_questions,
					'page_title'	:	'Send Survey Email',
				}
				messages.error(request, 'Opps! Sorry looks like we faced an error while updating your survey. Please contact admin support for further information')
				return render(request, self.template_name, context)

			for answer in question.get_question_choices():
				try:
					answer.answer_statement = request.POST.get('question-'+str(question.question_no)+'-answer-'+str(answer.pk))
					answer.save()

				except Exception as exc:
					print('Error! ',exc)
					context = {
						'survey_obj'	:	survey_obj,
						'survey_questions'	:	survey_questions,
						'page_title'	:	'Send Survey Email',
					}
					messages.error(request, 'Opps! Sorry looks like we faced an error while updating your survey. Please contact admin support for further information')
					return render(request, self.template_name, context)
				

		messages.success(request, 'Survey details updated successfuly')
		return redirect('surveyscaled:survey-created', survey_obj.slug)

# View for closing active surveys (User created)
def CloseSurveyView(request, slug):
	if request.method == 'GET':
		survey_obj = Survey.objects.get(slug=slug)
		survey_obj.is_active = False
		survey_obj.save()
		messages.success(request, 'Survey status changed successfuly. No more survey response allowed for this survey now')
		return redirect('surveyscaled:survey-list')
	else:
		messages.error(request, 'Request method not supported')
		return redirect('surveyscaled:survey-list')

# 
class ThirdPartySurveyListView(ListView):
    model = Survey_Metas
    paginate_by = 15
    context_object_name = 'surveys'
    template_name = 'survey_list.html'
    ordering = ['-survey_id']

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = 'Imported Survey List'
        context["page"] = 'thirdparty'
        return context

# View to load page for 3rd survey importing and saving data of imported file
class UploadSurveyResponse(View):
	template_name = 'upload_survey_response.html'

	def get(self, request):
		context = {
			'page_title'	:	'Upload Survey Response',
		}
		return render(request, self.template_name, context)

	def post(self, request):
		file = request.FILES['response-file']
		form_lenght = int(request.POST.get('form-length', None))
		survey_name = request.POST.get('survey_name', None)
		meta_obj = Survey_Metas(survey_name=survey_name, file_name=file)
		meta_obj.save()
		total_reponses = 0
		if settings.DEBUG:
			# Reading file from media files in django
			df = pd.read_csv(meta_obj.file_name, sep=',')

		else:
			# Reading file saved in AWS S3 Bucket
			FORECAST_DATA_OBJECT = meta_obj.file_name.name
			s3 = boto3.client(
			    's3',
			    aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
			    aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
			)
			obj = s3.get_object(Bucket=settings.AWS_STORAGE_BUCKET_NAME, Key=FORECAST_DATA_OBJECT)
			data = obj['Body'].read().decode('utf-8')

			df=pd.read_csv(io.StringIO(data), sep=',')

		for x in range(form_lenght):
			select_value = request.POST.get('select_value_' + str(x), None)
			is_target = request.POST.get('is_target_' + str(x), None)
			target_value = request.POST.get('target_value_' + str(x), None)
			is_demographics = request.POST.get('is_demographics_' + str(x), None)
			is_freeform = request.POST.get('is_freeform_' + str(x), None)
			# question_id = 
			question = request.POST.get('unique_question_' + str(x), None)
			abbreviation = request.POST.get('survey_abbreviation_' + str(x), None)
			question_type = request.POST.get('survey_question_type_' + str(x), None)
			survey_obj = Survey_Metas_Questions(
				survey_no = meta_obj,
				select_value = select_value,
				is_target = is_target,
				target_value = target_value,
				is_demographics = is_demographics,
				is_freeform = is_freeform,
				question = question,
				abbreviation = abbreviation,
				question_type = question_type,
			)
			survey_obj.save()

			row_iter = df.iterrows()
			bulk_mgr = BulkCreateManager(chunk_size=100)
			for index, row in row_iter:
				if survey_obj.question == row['Survey_question_description']:
					try:
						date = datetime.strptime(row['Survey_question_date'], '%Y/%m/%d')
						
					except:
						try:
							date = datetime.strptime(row['Survey_question_date'], '%Y-%m-%d')

						except:
							date = datetime.strptime(row['Survey_question_date'], '%d-%m-%Y')

					bulk_mgr.add(Survey_Metas_Answers(
							survey_no=meta_obj, 
							question_no=survey_obj, 
							question_date=date, 
							responder_id=row['Responder_id'], 
							question_statement=row['Survey_question_description'], 
							question_answer=row['Survey_answer_to_question']
						)
					)

					# Counting total responses for the imported survey
					total_reponses += 1

			bulk_mgr.done()

			meta_obj.activated = True
			meta_obj.total_reponses = total_reponses
			meta_obj.save()

		messages.success(request, 'Survey response uploaded successfuly')
		return redirect('surveyscaled:third-party-survey-list')

# View to handle handle the file uploaded by user for survey response upload page
class SurveyResponseFileQuestionsView(View):
	def post(self, request, *args, **kwargs):
		file = request.FILES['response-file']
		csv_obj = CSV(file_name=file, activated=False)
		csv_obj.save()
		questions = []
		answers = []
		# Opening csv file
		if settings.DEBUG:
			# Reading file from media files in django
			df = pd.read_csv(csv_obj.file_name, sep=',')

		else:
			# Reading file saved in AWS S3 Bucket
			FORECAST_DATA_OBJECT = csv_obj.file_name.name
			s3 = boto3.client(
			    's3',
			    aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
			    aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
			)
			obj = s3.get_object(Bucket=settings.AWS_STORAGE_BUCKET_NAME, Key=FORECAST_DATA_OBJECT)
			data = obj['Body'].read().decode('utf-8')
			
			df=pd.read_csv(io.StringIO(data), sep=',')

		row_iter = df.iterrows()
		print('Book:  ',df)
		for index, row in row_iter:
			if 'Survey_question_date' in df.columns and 'Responder_id' in df.columns and 'Survey_question_description' in df.columns and 'Survey_answer_to_question' in df.columns:
				pass
			else:
				return JsonResponse({"success": False, "message": "File format is not correct"}, safe=False)

			questions.append(row['Survey_question_description'])

		new_questions = get_unique_questions(questions)
		file_name = Path(str(csv_obj.file_name)).stem
		for question in new_questions:
			answers.append(get_answers_list(question, df))

		csv_obj.file_name.delete()	
		csv_obj.delete()
		return JsonResponse({"success": True, "message": "Loaded", 'questions': new_questions, 'answers': answers, 'file_name': file_name}, safe=False)

# Function to get answer list for each question in 3rd party survey import
def get_answers_list(question, df):
	answers = []

	row_iter = df.iterrows()
		
	for index, row in row_iter:
		if row['Survey_question_description'] == question:
			answers.append(row['Survey_answer_to_question'])

	answers = get_unique_questions(answers)
	answers.insert(0 , question)
	return answers


# Function to find unique question from the file uploaded as 3rd party survey import
def get_unique_questions(questions):
    list_of_unique_questions = []

    unique_questions = set(questions)

    for question in unique_questions:
        list_of_unique_questions.append(question)

    return list_of_unique_questions


# class SurveyAnalysisView(View):
# 	template_name = 'survey_dashboard.html'
	
# 	def get(self, request, slug):
# 		survey = Survey_Metas.objects.get(slug=slug)
# 		labels = []
# 		questions_number = 0
# 		# 1D array list to survey questions response data
# 		response_data = np.array([], dtype='int16')

# 		# if survey.question_sacle == '1-10':
# 		labels = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
# 		chart_type = 'bar'
# 		length = 10
# 		# elif survey.question_sacle == '1-5':
# 		# 	labels = [1, 2, 3, 4, 5]
# 		# 	chart_type = 'bar'
# 		# 	length = 5
# 		# elif survey.question_sacle == '1-4':
# 		# 	labels = [1, 2, 3, 4]
# 		# 	chart_type = 'bar'
# 		# 	length = 4
# 		# elif survey.question_sacle == '1-2':
# 		# 	labels = ['No', 'Yes']
# 		# 	chart_type = 'pie'
# 		# 	length = 2

# 		for question in survey.get_questions_list():
# 			question_response = np.array([], dtype='int16')
# 			answer_list = Survey_Metas_Answers.objects.filter(survey_no=survey, question_no=question.pk).values_list('question_answer', flat = True).annotate(total_responses=Count('question_answer'))
# 			answer_response_count = Survey_Metas_Answers.objects.filter(survey_no=survey, question_no=question.pk).values_list('question_answer', flat = False).annotate(total_responses=Count('question_answer'))
# 			questions_number += 1

# 			print('Answer list: ',answer_list)
# 			print('Answer Response Count: ',answer_response_count)

# 			for label in labels:
# 				added = False
# 				for answer in answer_response_count:
# 					if label == int(answer[0]):
# 						percent = int(answer[1])/survey.total_reponses * 100
# 						question_response = np.append(
# 							question_response,
# 							[
# 								round(percent)
# 							]
# 						)
# 						added = True

# 				if added is False:
# 					question_response = np.append(
# 						question_response,
# 						[
# 							round(0)
# 						]
# 					)


			
			
# 			response_data = np.append(
# 				response_data, 
# 				[
# 					question_response
# 				]
# 			)
		
# 		print('Response: ',response_data)
# 		print('Question Number ',questions_number)

# 		# Reshaping the 1D array list to multidimension array list
# 		response_data = np.reshape(
# 			response_data,     # the array to be reshaped
# 			(questions_number,length)  # dimensions of the new array
# 		)

# 		#Paginating survey list
# 		page = request.GET.get('page', 1)
# 		paginator = Paginator(survey_obj, 2)
# 		try:
# 			survey_list = paginator.page(page)
# 		except PageNotAnInteger:
# 			survey_list = paginator.page(1)
# 		except EmptyPage:
# 			survey_list = paginator.page(paginator.num_pages)

# 		context = {
# 			'title'	:	'Surveyscaled - Dashboard',
# 			'survey_obj'	:	survey_obj,
# 			'previous_month_surveys_obj'	:	previous_month_surveys_obj,
# 			'growth_over_previous_month'	:	growth_over_previous_month,
# 			'new_survey_count'	:	this_month_surveys_obj.count(),
# 			'active_surveys'	:	active_surveys,
# 			'survey'		:	survey,
# 			'response_data'	:	response_data,
# 			# 'labels'		:	labels,
# 			'survey_list'	:	survey_list,
# 			'chart_type'	:	chart_type,
# 		}
# 		return render(request, self.template_name, context)


class SendEmailView(View):
	template_name = ''

	def post(self, request, slug):
		survey_obj = Survey.objects.get(slug=slug)
		current_user = request.user
		# Getting clients subscription details
		try:
			subscription_obj = SubscriptionsDetails.objects.get(user=current_user)

		except Exception as exc:
			messages.error(request, 'Please add you subscription details first')
			return redirect('surveyscaled:survey-created', survey_obj.slug)
		
		if settings.DEBUG:
			user_file = request.FILES.get('email-list', None)
			link_file = request.FILES.get('link-email-list', None)
			if user_file:
				file = user_file
				html_mail_template = 'email_templates/survey_email.html'
			elif link_file:
				file = link_file
				html_mail_template = 'email_templates/survey_link_email.html'

			csv_obj = CSV(file_name=file, survey_no=survey_obj, activated=False)
			csv_obj.save()

			# Reading file from media files in django
			df = pd.read_csv(csv_obj.file_name, sep=',')
			row_iter = df.iterrows()

			for index, row in row_iter:
				print('Inside email for smtp')
				user_name = row['fullname'].capitalize()
				user_email = row['email']
				# Getting domain data if exist
				try:
					domain = Site.objects.get_current().domain
				
				except Exception as exc:
					print('Error: ',exc)
					messages.error(request, 'Could not found any site information from database. Please go to Django admin panel and add site domain details in "Sites Table".')
					return redirect('surveyscaled:survey-created', survey_obj.slug)
				# Creating survey response page url for email template
				path = '/upload-survey/' + str(slug) + '/' + str(user_name)
				url = 'http://{domain}{path}'.format(domain=domain, path=path)
				# Dictionary used in email template to provide information
				context = {
					'user_name'	:	user_name,
					'url'		:	url,
				}

				try:
					email_template = get_template(html_mail_template).render(context)
					email_msg = EmailMessage(
						'We’d love your help! Fill out the quick survey and help us make our services better', # Subject
						email_template,
						settings.APPLICATION_EMAIL,
						[user_email],
						reply_to = [settings.APPLICATION_EMAIL]
					)
					email_msg.content_subtype = 'html'
					email_msg.send(fail_silently=False)

				except Exception as exc:
					print('Exception error at 833: ',exc)

		else:
			# Reading file saved in AWS S3 Bucket
			FORECAST_DATA_OBJECT = csv_obj.file_name.name
			s3 = boto3.client(
			    's3',
			    aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
			    aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
			)
			obj = s3.get_object(Bucket=settings.AWS_STORAGE_BUCKET_NAME, Key=FORECAST_DATA_OBJECT)
			data = obj['Body'].read().decode('utf-8')
			spamreader = csv.reader(io.StringIO(data), delimiter=',', quotechar='|')

			df = pd.read_csv(io.StringIO(data), sep=',')

			# Calling Mailchimp campaign creationa and submission functions
			mailchimp_marketing_api.StartMailChimpCampaignProcess(settings.MAILCHIMP_EMAIL_LIST_ID,
				'1',
				'1',
				settings.MAILCHIMP_API_KEY,
				settings.MAILCHIMP_DATA_CENTER,
				survey_obj.name,
				df,
				email_template = get_template(html_mail_template).render(context)
			)
				
		csv_obj.activated = True
		csv_obj.save()
		messages.success(request, 'Survey link sent to users')
		return redirect('surveyscaled:survey-created', survey_obj.slug)


class UploadSurveyView(View):
	template_name = 'survey_answers.html'
	form_class = UserDetailsForm

	def get(self, request, slug, user):
		user_form = self.form_class
		try:
			survey_obj = Survey.objects.get(slug=slug, is_active=True)
		except Exception as e:
			html = "<center><h3>We are extremly sorry! The survey you are looking for is not availible any more. Sorry for the inconvenience.</center>"
			return HttpResponse(html)

		context = {
			'page_title'	:	'Respond to Survey',
			'user'			:	user,
			'survey'		:	survey_obj,
			'user_form'		:	user_form,
		}
		return render(request, self.template_name, context)

	def post(self, request, slug, user):
		user_form = self.form_class(request.POST or None)
		survey_obj = Survey.objects.get(slug=slug)
		survey_questions = SurveyQuestions.objects.filter(survey_no=survey_obj)

		if user_form.is_valid():
			form_data = user_form.save(commit=False)
			form_data.name = user
			form_data.save()
			form_data.responder_id = form_data.pk
			form_data.save()

			for question in survey_questions:
				# getting question responses from front-end
				if question.question_type == 'Multiple Choices - Select One Answer' or question.question_type == 'Multiple Choices - Select All That Applies':
					answer = request.POST.getlist('question-number-'+str(question.pk)+'-answer')
					for value in answer:
						answer_obj = SurveyAnswers(survey_no=survey_obj, question_no=question.question_no, question_statement=question.question_statement, responder_id=form_data.responder_id, question_answer=value, question_type=question.question_type)
						answer_obj.save()

				else:
					answer = request.POST['question-number-'+str(question.pk)+'-answer']
					answer_obj = SurveyAnswers(survey_no=survey_obj, question_no=question.question_no, question_statement=question.question_statement, responder_id=form_data.responder_id, question_answer=answer, question_type=question.question_type)
					answer_obj.save()

			survey_obj.total_reponses += 1
			survey_obj.save()
			return redirect('surveyscaled:thank-you-page')

		else:
			messages.error(request, 'Please fix the errors below')
			context = {
				'page_title'	:	'Respond to Survey',
				'user'			:	user,
				'survey'		:	survey_obj,
				'user_form'		:	user_form,
			}
			return render(request, self.template_name, context)

def ThankyouView(request):
	return render(request, 'thank_you.html')


