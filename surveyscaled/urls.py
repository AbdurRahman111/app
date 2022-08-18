from django.urls import path, include
from . import views

app_name = 'surveyscaled'

urlpatterns = [
	path('dashboard', views.SurveyDashboardView.as_view(), name='survey-dashboard'),
	path('api/survey-response/<pk>', views.SurveyResponseAPIView, name='get-survey-api'),
	path('create-survey', views.CreateSurveyView.as_view(), name='create-survey'),
	path('survey/<slug:slug>', views.EditSurveyView.as_view(), name='survey-created'),
	path('close-survey/<slug:slug>', views.CloseSurveyView, name='close-survey'),
	path('survey-list', views.SurveyListView.as_view(), name='survey-list'),
	path('third-party-survey-list', views.ThirdPartySurveyListView.as_view(), name='third-party-survey-list'),
	path('ingest-data', views.UploadSurveyResponse.as_view(), name='ingest-data'),
	path('send-email/<slug:slug>', views.SendEmailView.as_view(), name='send-email'),
	path('upload-survey/<slug:slug>/<str:user>', views.UploadSurveyView.as_view(), name='upload-survey'),
	path('thank-you', views.ThankyouView, name='thank-you-page'),
	path('survey-reponse-file', views.SurveyResponseFileQuestionsView.as_view(), name='survey-reponse-file'),
	# path('survey/analysis/<slug>', views.SurveyAnalysisView.as_view(), name='survey-analysis'),
]