from django import forms
from django.forms import formset_factory
from .models import (
	UserDetails,
	Survey,
	SurveyQuestions,
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

class UserDetailsForm(forms.ModelForm):
	gender = forms.CharField(
		widget=forms.RadioSelect(choices=Gender_Options),
	)
	age = forms.CharField(
		widget=forms.RadioSelect(choices=Age_Options),
	)
	children_under_eighteen = forms.CharField(
		widget=forms.RadioSelect(choices=Children_Under_18_Options),
	)
	number_of_children = forms.IntegerField(initial ='')
	martial_status = forms.CharField(
		widget=forms.RadioSelect(choices=Marital_Options),
	)
	employement_status = forms.CharField(
		widget=forms.RadioSelect(choices=Employement_Options),
	)

	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.fields['number_of_children'].widget.attrs.update({'class': 'form-control textinput mt-2', 'min': '0', 'blank': 'true' , 'null': 'true', 'required': 'false'})

	class Meta:
		model = UserDetails
		fields = ['gender', 'age', 'children_under_eighteen', 'number_of_children', 'martial_status', 'employement_status']

class SurveyForm(forms.ModelForm):
	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.fields['name'].widget.attrs.update({'class': 'form-control textinput', 'pattern' : '[a-zA-Z0-9\s]{1,250}', 'title' : 'Alphabets, Integers and Spaces only', 'placeholder': 'Enter the name of the survey'})

	class Meta:
		model = Survey
		fields = ['name', 'survey_purpose']
		widgets = {
		    'survey_purpose' : forms.Textarea(
		        attrs = {
		            'class' : 'textinput form-control',
		            'rows'  : '4',
		            'placeholder': 'Enter the purpose of the survey'
		        }
		    )
		}


class SurveyQuestionsForm(forms.ModelForm):
	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.fields['question_no'].widget.attrs.update({'class': 'form-control textinput', 'pattern' : '[a-zA-Z0-9\s]{1,250}', 'title' : 'Alphabets, Integers and Spaces only', 'placeholder': 'Enter question number'})

	class Meta:
		model = SurveyQuestions
		fields = ['question_no', 'question_statement']
		widgets = {
		    'question_statement' : forms.Textarea(
		        attrs = {
		            'class' : 'textinput form-control',
		            'rows'  : '4',
		            'placeholder': 'Enter question statement'
		        }
		    )
		}

SurveyQuestionsFormset = formset_factory(SurveyQuestionsForm, extra=3)