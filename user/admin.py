from django.contrib import admin
from .models import CustomUser, Evaluation, TrainingApplications
from .forms import CustomUserForm, EvaluationForm 

class CustomUserAdmin(admin.ModelAdmin):
    form = CustomUserForm

class CustomEvaluation(admin.ModelAdmin):
    form = EvaluationForm

# class TrainingAdmin(admin.ModelAdmin):
#     prepopulated_fields = {"employee_name": ["employee_name",]}

admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(Evaluation, CustomEvaluation)
admin.site.register(TrainingApplications)