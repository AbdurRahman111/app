from django.contrib import admin

from .models import (
    UserDetails,
    CompanyEmailDetails,
	Survey,
    SurveyQuestions,
    SurveyAnswers,
    CSV,
    Survey_Metas,
    Survey_Metas_Questions,
    Survey_Metas_Answers,
)

class CompanyEmailDetailsFilter(admin.ModelAdmin):
    list_display = ('id', 'comapny_name', 'comapny_address', 'comapny_city', 'comapny_city_zip', 'company_country', 'survey_invite_subject', 'survey_invite_message')

class UserDetailsFilter(admin.ModelAdmin):
    list_display = ('id', 'responder_id', 'name', 'gender', 'age', 'children_under_eighteen', 'number_of_children', 'martial_status', 'employement_status', 'slug')
    search_fields = ["name"]
    list_filter = ('children_under_eighteen', 'martial_status', 'employement_status')

class SurveyFilter(admin.ModelAdmin):
    list_display = ('survey_no', 'name', 'survey_purpose', 'company_id', 'subscription_id', 'created_by', 'total_reponses', 'created_on', 'updated_on', 'is_active', 'slug')
    search_fields = ["name"]
    list_filter = ['is_active', 'created_on']

class SurveyQuestionsFilter(admin.ModelAdmin):
    list_display = ('id', 'survey_no', 'question_no', 'question_statement', 'question_type', 'scale_type', 'created_on', 'updated_on')
    search_fields = ["question_statement"]
    list_filter = ['created_on', 'question_type']

class SurveyQuestionsAnswerFilter(admin.ModelAdmin):
    list_display = ('id', 'survey_no', 'question_no', 'answer_statement')
    search_fields = ["answer_statement"]

class SurveyAnswersFilter(admin.ModelAdmin):
    list_display = ('id', 'responder_id', 'survey_no', 'question_no', 'question_statement', 'question_answer', 'question_type', 'answered_at')
    search_fields = ["question_statement"]
    list_filter = ['answered_at']

class OutsideSurveyFilter(admin.ModelAdmin):
    list_display = ('survey_id', 'survey_name', 'total_reponses', 'file_name', 'activated', 'slug',)
    search_fields = ["survey_name"]

class OutsideSurveyAnswersFilter(admin.ModelAdmin):
    list_display = ('survey_no', 'responder_id', 'answered_at', 'question_no', 'question_date', 'question_statement', 'question_answer')
    search_fields = ["question"]
    list_filter = ['answered_at']

class OutsideSurveyQuestionsFilter(admin.ModelAdmin):
    list_display = ('pk', 'survey_no', 'question_id', 'question', 'question_type', 'abbreviation', 'select_value', 'is_target', 'target_value', 'is_demographics', 'is_freeform')
    search_fields = ["question"]
    list_filter = ['question_type']

class CSVFilter(admin.ModelAdmin):
    list_display = ('id', 'file_name', 'survey_no', 'uploaded', 'activated')
    search_fields = ["file_name"]
    list_filter = ['activated']


admin.site.register(UserDetails, UserDetailsFilter)
admin.site.register(CompanyEmailDetails, CompanyEmailDetailsFilter)
admin.site.register(Survey, SurveyFilter)
admin.site.register(SurveyQuestions, SurveyQuestionsFilter)
admin.site.register(SurveyAnswers, SurveyAnswersFilter)
admin.site.register(CSV, CSVFilter)
admin.site.register(Survey_Metas, OutsideSurveyFilter)
admin.site.register(Survey_Metas_Questions, OutsideSurveyQuestionsFilter)
admin.site.register(Survey_Metas_Answers, OutsideSurveyAnswersFilter)