from django.urls import path, include
from . import views
from dal import autocomplete
from .models import Experiment

app_name = 'experiment'

urlpatterns = [
	# Auto select experiment field url
	path('experiment-autocomplete', views.ExperimentAutoComplete.as_view(model=Experiment), name='experiment-autocomplete'),
	path('dashboard', views.ExperimentsDashboardView.as_view(), name='experiment-dashboard'),
	path('ingest-data', views.UploadClosedExperimentView.as_view(), name='upload-experiment'),
	path('create-test/email-experiment', views.CreateEmailExperimentView.as_view(), name='create-email-experiment'),
	path('create-test/display-experiment', views.CreateDisplayExperimentView.as_view(), name='create-display-experiment'),
	path('create-test/file-rendering', views.FileRenderingVidew, name='file-rendering'),
	path('experiment_list', views.ExperimentListView.as_view(), name='experiment-list'),
	path('execute-email-experiment', views.ExecuteEmailExperimentView.as_view(), name='execute-email-experiment')
]
