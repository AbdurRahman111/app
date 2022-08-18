from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Profile

Gender_Option = [
    ('Male', 'Male'),
    ('Female', 'Female'),
    ('Do not want to respond', 'Do not want to respond')
]

# Custom Widget for to display a Datepicker
class DateInput(forms.DateTimeInput):
    input_type = 'date'


# Sign Up Form
class SignUpForm(UserCreationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update({'placeholder': 'Username'})
        self.fields['password1'].widget.attrs.update({'placeholder': 'Password'})
        self.fields['password2'].widget.attrs.update({'placeholder': 'Confirm Password'})

    class Meta:
        model = User
        fields = [
                'username', 
                'password1', 
                'password2', 
            ]

class UserUpdateForm(forms.ModelForm):
    first_name = forms.CharField(label='First Name', required=True, max_length=100)
    last_name = forms.CharField(label='Last Name', required=True, max_length=100)
    email = forms.EmailField()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['first_name'].widget.attrs.update({'placeholder': 'First name', 'class': 'form-control textinput',})
        self.fields['last_name'].widget.attrs.update({'placeholder': 'Last name', 'class': 'form-control textinput',})
        self.fields['email'].widget.attrs.update({'placeholder': 'Email', 'class': 'form-control textinput',})

    class Meta:
        model = User
        fields = [  
            'first_name',
            'last_name',
            'email',
        ]


class ProfileUpdateForm(forms.ModelForm):
    date_of_birth= forms.DateField(label='Date of Birth', required=True, widget=DateInput(attrs={'class':'form-control',  'id':'startdate'}))
    gender = forms.ChoiceField(choices = Gender_Option, required=True, widget=forms.RadioSelect())

    class Meta:
        model = Profile
        fields =[
            'date_of_birth',
            'gender',
            'profile_image',
        ]