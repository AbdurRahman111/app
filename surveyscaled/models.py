from django.db import models
from survey.utils import unique_slug_generator
from django.db.models.signals import pre_save
import uuid
from django.db.models import Count
from django.contrib.auth.models import User

Question_Type = (
	('Yes/No Question', 'Yes/No Question'),
	('Scaled Question', 'Scaled Question'),
	('Scaled Question - Customer Satisfaction Survey', 'Scaled Question - Customer Satisfaction Survey'),
	('Scaled Question - Net Promoter Survey', 'Scaled Question - Net Promoter Survey'),
	('Multiple Choices - Select One Answer', 'Multiple Choices - Select One Answer'),
	('Multiple Choices - Select All That Applies', 'Multiple Choices - Select All That Applies'),
	('Free Form', 'Free Form'),
)

Scale_Type = (
    ('1-10','1-10 Worst to Best'),
    ('1-5','1-5 Worst to Best'),
    ('1-4','1-4 Worst to Best'),
)

Gender_Options = (
    ('Male','Male'),
    ('Female','Female'),
)

Age_Options = (
    ('Under 18','Under 18'),
    ('18-24','18-24'),
    ('25-34','25-34'),
    ('35-44','35-44'),
    ('45-54','45-54'),
    ('55-64','55-64'),
    ('65 or Above','65 or Above'),
)

Children_Under_18_Options = (
    ('Yes','Yes'),
    ('No','No'),
)

Marital_Options = (
    ('Single, Not Married','Single, Not Married'),
    ('Married','Married'),
    ('Living with partner','Living with partner'),
    ('Separated','Separated'),
    ('Divorced','Divorced'),
    ('Widowed','Widowed'),
    ('Prefer not to answer','Prefer not to answer'),
)

Employement_Options = (
    ('Employed full time','Employed full time'),
    ('Employed half time','Employed half time'),
    ('Unemployed','Unemployed'),
)

Improted_Survey_Question_Type = (
	('Demographics','Demographics'),
	('Free Form','Free Form'),
    ('Scaled Answers','Scaled Answers'),
    ('Multiple Choice - Select one','Multiple Choice - Select one'),
    ('Select All that Applies','Select All that Applies'),
)

class CompanyEmailDetails(models.Model):
	comapny_name = models.CharField(max_length=250, verbose_name = 'Company Name')
	comapny_address = models.CharField(max_length=500, verbose_name = 'Company Address')
	comapny_city = models.CharField(max_length=50, verbose_name = 'City')
	comapny_city_zip = models.CharField(max_length=50, verbose_name = 'Zip Code')
	company_country = models.CharField(max_length=100, verbose_name = 'Country')
	survey_invite_subject = models.CharField(max_length=250, verbose_name = 'Survey Invitation Email Subject')
	survey_invite_message = models.CharField(max_length=1000, verbose_name = 'Survey Invitation Email Message')

	def __str__(self):
		return self.comapny_name

	class Meta:
		verbose_name_plural = "Company Details"


class UserDetails(models.Model):
	responder_id = models.CharField(max_length=250, blank=True, null=True)
	name = models.CharField(max_length=250, verbose_name = 'Name')
	gender = models.CharField(max_length=6, choices=Gender_Options, verbose_name = 'Gender')
	age = models.CharField(max_length=20, choices=Age_Options, verbose_name = 'Age')
	children_under_eighteen = models.CharField(max_length=5, choices=Children_Under_18_Options, verbose_name = 'Children Under 18')
	number_of_children = models.IntegerField(blank=True, null=True, default=0)
	martial_status = models.CharField(max_length=50, choices=Marital_Options, verbose_name = 'Marital Status')
	employement_status = models.CharField(max_length=50, choices=Employement_Options, verbose_name = 'Employement Status')
	slug = models.SlugField(blank=True, null=True)

	def __str__(self):
		return self.name

	class Meta:
		verbose_name_plural = "User Details"


# Model to save details for the survey
class Survey(models.Model):
	survey_no = models.AutoField(primary_key=True, verbose_name = 'Survey #')
	name = models.CharField(max_length=1000, verbose_name = 'Survey Name')
	survey_purpose = models.CharField(max_length=5000, verbose_name = 'Survey Purpose')
	created_on = models.DateTimeField(auto_now_add=True, auto_now=False, verbose_name = 'Creation Date')
	updated_on = models.DateTimeField(auto_now_add=False, auto_now=True, verbose_name = 'Last Update Date')
	is_active = models.BooleanField(default=True)
	total_reponses = models.IntegerField(default=0)
	company_id = models.CharField(max_length=150, verbose_name='Company Id')
	subscription_id = models.CharField(max_length=150, verbose_name='Subscription Id')
	created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='created_by', verbose_name='Created By')
	slug = models.SlugField(max_length=1000, blank=True, null=True, verbose_name = 'Slug')

	def __str__(self):
		return self.name

	class Meta:
		ordering = ["-survey_no"]
		verbose_name_plural = "Surveys"

	def get_questions_list(self):
		return SurveyQuestions.objects.filter(survey_no=self).order_by('question_no')

	def get_questions_list_for_dashboard(self):
		return SurveyQuestions.objects.filter(survey_no=self).exclude(question_type='Free Form').order_by('question_no')

	def get_answers_list(self):
		return SurveyAnswers.objects.filter(survey_no=self)

	def get_total_number_of_questions(self):
		return SurveyQuestions.objects.filter(survey_no=self).count()

# Model to save questions for the survey
class SurveyQuestions(models.Model):
	id = models.AutoField(primary_key=True, verbose_name='Question ID')
	survey_no = models.ForeignKey(Survey, on_delete=models.CASCADE, related_name='questions_survey', verbose_name = 'Survey #')
	question_no = models.CharField(max_length=50, verbose_name = 'Question #')
	question_statement = models.CharField(max_length=5000, verbose_name = 'Question Statement')
	question_type = models.CharField(max_length=50, choices=Question_Type, verbose_name = 'Question Type')
	scale_type = models.CharField(max_length=20, choices=Scale_Type, blank=True, null=True, verbose_name = 'Scale Type')
	number_of_answers = models.IntegerField(blank=True, null=True, verbose_name='Number of Answers')
	created_on = models.DateTimeField(auto_now_add=True, auto_now=False, verbose_name = 'Creation Date')
	updated_on = models.DateTimeField(auto_now_add=False, auto_now=True, verbose_name = 'Last Update Date')

	def __str__(self):
		return f'Survey # {self.survey_no}, Question # {self.question_no}'

	def get_answers_list(self):
		return SurveyAnswers.objects.filter(survey_no=self.survey_no, question_no=self.question_no)

	def get_question_choices(self):
		return SurveyQuestionAnswers.objects.filter(question_no=self)

	def get_response_answers_count(self):
		answer_list = SurveyAnswers.objects.filter(survey_no=self.survey_no, question_no=self.question_no).values_list('question_answer', flat = False).annotate(total_responses=Count('question_answer'))
		return answer_list

	class Meta:
		ordering = ["-survey_no"]
		verbose_name_plural = "Survey's Questions"

# Model to save questions for the survey
class SurveyQuestionAnswers(models.Model):
	id = models.AutoField(primary_key=True, verbose_name='Answer ID')
	survey_no = models.ForeignKey(Survey, on_delete=models.CASCADE, related_name='question_answers_survey', verbose_name = 'Survey #')
	question_no = models.ForeignKey(SurveyQuestions, on_delete=models.CASCADE, related_name='answers_question', verbose_name = 'Question #')
	answer_statement = models.CharField(max_length=5000, verbose_name = 'Question Statement')

	def __str__(self):
		return f'Question # {self.question_no}, Answer # {self.id}'

	def get_answers_list(self):
		return SurveyAnswers.objects.filter(survey_no=self.survey_no, question_no=self.question_no)

	class Meta:
		ordering = ["-survey_no"]
		verbose_name_plural = "Survey Question's Answers"

# Model to save questions for the survey
class SurveyAnswers(models.Model):
	survey_no = models.ForeignKey(Survey, on_delete=models.CASCADE, related_name='survey_num', verbose_name = 'Survey #', blank=True, null=True)
	question_no = models.CharField(max_length=50, verbose_name = 'Question #')
	question_statement = models.CharField(max_length=1000, verbose_name = 'Question Statement')
	responder_id = models.CharField(max_length=250, verbose_name = 'Responder Id')
	answered_at = models.DateTimeField(auto_now_add=True, auto_now=False, verbose_name = 'Answer Date')
	question_answer = models.CharField(max_length=250, verbose_name = 'Question Answer')
	question_type = models.CharField(max_length=50, verbose_name='Question Type')

	def __str__(self):
		return f'{self.survey_no} {self.question_no}'

	class Meta:
		ordering = ["-survey_no"]
		verbose_name_plural = "Survey Answers"

# Model to save details for the survey
class Survey_Metas(models.Model):
	survey_id = models.AutoField(primary_key=True, verbose_name = 'Survey #')
	file_name = models.FileField(upload_to='csvs')
	uploaded = models.DateTimeField(auto_now_add=True)
	activated = models.BooleanField(default=False)
	total_reponses = models.IntegerField(default=0)
	survey_name = models.CharField(max_length= 500, verbose_name = 'Survey Name')
	slug = models.SlugField(max_length=500, blank=True, null=True, verbose_name = 'Slug')

	def __str__(self):
		return self.survey_name

	class Meta:
		ordering = ["-survey_id"]
		verbose_name_plural = "Survey_Metas"

	def get_questions_list(self):
		return Survey_Metas_Questions.objects.filter(survey_no=self)

	def get_answers_list(self):
		return Survey_Metas_Answers.objects.filter(survey_no=self)

class Survey_Metas_Questions(models.Model):
	survey_no = models.ForeignKey(Survey_Metas, on_delete=models.CASCADE, related_name='survey_meta_number', verbose_name='Survey #')
	select_value = models.CharField(max_length=50, verbose_name = 'Select Value')
	is_target = models.CharField(max_length=1, verbose_name = 'Is Target')
	target_value = models.CharField(max_length=2, null=True, blank=True, verbose_name = 'Target Value')
	is_demographics = models.CharField(max_length=1, verbose_name='Is_Demographics')
	is_freeform = models.CharField(max_length=1, verbose_name='Is_FreeForm')
	question_id = models.CharField(max_length=40, blank=True, unique=True, default=uuid.uuid4, verbose_name = 'Question #')
	question = models.CharField(max_length=1000, verbose_name = 'Question')
	abbreviation = models.CharField(max_length=150, verbose_name = 'Abbreviation')
	question_type = models.CharField(max_length=40, choices=Improted_Survey_Question_Type, verbose_name='Question Type')

	def __str__(self):
		return f'{self.survey_no} {self.pk}'

	class Meta:
		ordering = ["-survey_no"]
		verbose_name_plural = "Survey Meta Questions"


# Model to save questions for the survey
class Survey_Metas_Answers(models.Model):
	survey_no = models.ForeignKey(Survey_Metas, on_delete=models.CASCADE, related_name='survey_metas_detail', verbose_name = 'Survey #')
	responder_id = models.CharField(max_length=250, verbose_name = 'Responder Id')
	answered_at = models.DateTimeField(auto_now_add=True, auto_now=False, verbose_name = 'Answer Date')
	question_no = models.ForeignKey(Survey_Metas_Questions, on_delete=models.CASCADE, related_name='question_reference', verbose_name = 'Question #')
	question_date = models.DateField()
	question_statement = models.CharField(max_length=1000, verbose_name = 'Question Statement')
	question_answer = models.CharField(max_length=25, verbose_name = 'Question Answer')

	def __str__(self):
		return f'{self.survey_no}'

	class Meta:
		ordering = ["-id"]
		verbose_name_plural = "Survey_Metas_Answers"

class CSV(models.Model):
	file_name = models.FileField(upload_to='csvs')
	survey_no = models.ForeignKey(Survey, on_delete=models.CASCADE, blank=True, null=True, related_name='survey_number', verbose_name = 'Survey #')
	uploaded = models.DateTimeField(auto_now_add=True)
	activated = models.BooleanField(default=False)

	def __str__(self):
		return f"File Id: {self.id}"

	class Meta:
		ordering = ["-id"]
		verbose_name_plural = "Email CSV Files"

# generates slug value according to the instance name on save, update
def slug_generator(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = unique_slug_generator(instance)

pre_save.connect(slug_generator, sender=Survey)
pre_save.connect(slug_generator, sender=UserDetails)
pre_save.connect(slug_generator, sender=Survey_Metas)