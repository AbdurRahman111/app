from django.contrib import admin
from .models import (
	Experiment,
	ImportExperimentContent,
	ExperimentGroups,
)

class ExperimentFilters(admin.ModelAdmin):
	list_display = ('id', 'experiment_name', 'experiment_hypothesis', 'sender_email', 'email_subject', 'experiment_type',  'campaign_type', 'experiment_file', 'slug', 'is_active')
	list_filter = ('is_active', 'experiment_type', 'campaign_type')
	search_fields = ('experiment_name',)


class ImportExperimentContentFilters(admin.ModelAdmin):
	list_display = ('id', 'experiment', 'responder_id', 'experiment_content', 'response_datetime', 'experiment_launch_date',  'experiment_question_type', 'experiment_response_click', 'experiment_response_view', 'experiment_response_convert', 'experiment_metric_name', 'experiment_metric_value', 'experiment_group')
	list_filter = ('response_datetime', 'experiment_launch_date')
	search_fields = ('experiment_id',)

class ExperimentGroupsFilter(admin.ModelAdmin):
	list_display = ('id', 'experiment', 'file_type', 'file_name')


admin.site.register(Experiment, ExperimentFilters)
admin.site.register(ImportExperimentContent, ImportExperimentContentFilters)
admin.site.register(ExperimentGroups, ExperimentGroupsFilter)