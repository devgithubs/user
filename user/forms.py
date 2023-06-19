from django import forms
from django.contrib.auth.forms import UserCreationForm, PasswordResetForm
from .models import CustomUser, Evaluation, TrainingApplications

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Div, Field


class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ['username', 'password1', 'password2', 'is_staff', 'email', 'first_name', 'last_name', 'position', 'funded_by', 'annual_salary']

        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control'}),
            'password1': forms.PasswordInput(attrs={'class': 'form-control'}),
            'password2': forms.PasswordInput(attrs={'class': 'form-control'}),
            'is_staff': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
            'position': forms.TextInput(attrs={'class': 'form-control'}),
            'funded_by': forms.TextInput(attrs={'class': 'form-control'}),
            'annual_salary': forms.NumberInput(attrs={'class': 'form-control'}),
        }

class CustomPasswordResetForm(PasswordResetForm):
    username = forms.CharField(max_length=150)

    def clean_username(self):
        username = self.cleaned_data['username']
        try:
            CustomUser.objects.get(username=username)
        except CustomUser.DoesNotExist:
            raise forms.ValidationError("Invalid username")
        return username



class CustomUserForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        exclude = (
            'employee_id',
            'investment_report',
            'training',
            'evaluation',
            'groups',
            'user_permissions',
            'password1',
            'password2',  # Exclude password fields from the form
        )


# class EvaluationForm(forms.ModelForm):
#     CHOICES = [
#         (1, 'Strongly Disagree'),
#         (2, 'Disagree'),
#         (3, 'Neutral'),
#         (4, 'Agree'),
#         (5, 'Strongly Agree'),
#     ]
#     start_date = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))
#     end_date = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))
#     topic_relevant = forms.ChoiceField(choices=CHOICES, widget=forms.RadioSelect)
#     encouragement = forms.ChoiceField(choices=CHOICES, widget=forms.RadioSelect)
#     material_helpfulness = forms.ChoiceField(choices=CHOICES, widget=forms.RadioSelect)
#     objective_met = forms.ChoiceField(choices=CHOICES, widget=forms.RadioSelect)
#     time_sufficient = forms.ChoiceField(choices=CHOICES, widget=forms.RadioSelect)
#     expectation_met = forms.ChoiceField(choices=CHOICES, widget=forms.RadioSelect)

#     class Meta:
#         model = Evaluation
#         fields = '__all__'

#     def __init__(self, *args, **kwargs):
#         super().__init__(*args, **kwargs)
#         self.helper = FormHelper()
#         self.helper.layout = Layout(
#             Div(
#                 Field('employee'),
#                 Field('employee_name'),
#                 Field('job_title'),
#                 Field('training_course'),
#                 Field('training_provider'),
#                 Field('start_date'),
#                 Field('end_date'),
#                 Field('no_of_days'),
#                 Field('certification'),
#                 Field('certification_reason'),
#                 Field('objective'),
#                 Field('topics'),
#                 Field('usefulness'),
#                 Field('three_important_points'),
#                 Field('topic_relevant'),
#                 Field('encouragement'),
#                 Field('material_helpfulness'),
#                 Field('objective_met'),
#                 Field('time_sufficient'),
#                 Field('expectation_met'),
#                 css_class='form-check'
#             ),
#         )


class EvaluationForm(forms.ModelForm):
    CHOICES = [
        (1, 'Strongly Disagree'),
        (2, 'Disagree'),
        (3, 'Neutral'),
        (4, 'Agree'),
        (5, 'Strongly Agree'),
    ]
    topic_relevant = forms.ChoiceField(choices=CHOICES, widget=forms.RadioSelect)
    encouragement = forms.ChoiceField(choices=CHOICES, widget=forms.RadioSelect)
    material_helpfulness = forms.ChoiceField(choices=CHOICES, widget=forms.RadioSelect)
    objective_met = forms.ChoiceField(choices=CHOICES, widget=forms.RadioSelect)
    time_sufficient = forms.ChoiceField(choices=CHOICES, widget=forms.RadioSelect)
    expectation_met = forms.ChoiceField(choices=CHOICES, widget=forms.RadioSelect)

    class Meta:
        model = Evaluation
        exclude = ('training_application', 'employee')


class TrainingApplicationForm(forms.ModelForm):
    class Meta:
        model = TrainingApplications
        fields = '__all__'
        exclude = ['application_status']

    def __init__(self, *args, **kwargs):
        request = kwargs.pop('request', None)  # Pop the 'request' argument from kwargs
        super().__init__(*args, **kwargs)
        if request: # and request.user.is_authenticated
            user = request.user
            self.fields['employee_name'].initial = user
            self.fields['employee_position'].initial = user.position