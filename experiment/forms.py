from django import forms
from dal import autocomplete
from .models import Experiment

# form used to create auto select dropdown for experiments
class SelectExperimentForm(forms.ModelForm):
    experiment_name = forms.ModelChoiceField(
        queryset=Experiment.objects.all(),
        widget=autocomplete.ModelSelect2(url='experiment:experiment-autocomplete')
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['experiment_name'].widget.attrs.update({'class': 'textinput form-control'})
        
    class Meta:
        model = Experiment
        fields = ['experiment_name']