# Create your models here.
from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
    ROLES = (
        ('admin', 'Admin'),
        ('employee', 'Employee'),
    )

    role_name = models.CharField(max_length=10, choices=ROLES, null=True)
    email = models.CharField(max_length=45, null=True, unique=True)
    first_name = models.CharField(max_length=45, null=True)
    last_name = models.CharField(max_length=45, null=True)
    position = models.CharField(max_length=45, null=True)
    funded_by = models.CharField(max_length=45, null=True)
    annual_salary = models.DecimalField(max_digits=10, decimal_places=0, null=True)

    def is_admin(self):
        return self.role_name == 'admin'

    def is_employee(self):
        return self.role_name == 'employee'

    class Meta:
        db_table = 'custom_user'


class Evaluation(models.Model):
    employee = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    training_application = models.ForeignKey('TrainingApplications', on_delete=models.CASCADE, related_name='evaluation_record')
    employee_name = models.CharField(max_length=45)
    job_title = models.CharField(max_length=45)
    training_course = models.TextField()
    training_provider = models.TextField()
    start_date = models.DateField()
    end_date = models.DateField()
    no_of_days = models.IntegerField()
    certification = models.IntegerField()
    certification_reason = models.TextField()
    objective = models.TextField()
    topics = models.TextField()
    usefulness = models.TextField()
    three_important_points = models.TextField()
    topic_relevant = models.IntegerField()
    encouragement = models.IntegerField()
    material_helpfulness = models.IntegerField()
    objective_met = models.IntegerField()
    time_sufficient = models.IntegerField()
    expectation_met = models.IntegerField()
    completed = models.BooleanField(default=False)


    class Meta:
        db_table = 'evaluation'

    def __str__(self):
        return str(f"{self.training_course} - {self.employee_name}")
    

   
class TrainingApplications(models.Model):
    D_METHODS = (
        ('webinar', 'Webinar'),
        ('seminar', 'Seminar'),
        ('zoom', 'Zoom'),
        ('onsite','On Site')
    )
    employee_name = models.CharField(max_length=45, )
    employee_position = models.CharField(max_length=45)
    length_of_service = models.IntegerField()
    application_date = models.DateField()
    programme_name = models.CharField(max_length=45)
    training_provider = models.CharField(max_length=45)
    start_date = models.DateField()
    end_date = models.DateField()
    no_of_days = models.IntegerField()
    no_of_hours = models.IntegerField(null=True)
    delivery_method = models.CharField(choices=D_METHODS, max_length=45)
    programme_aims = models.TextField()
    programme_objectives = models.TextField()
    expected_outcome = models.TextField()
    bjc_contribution = models.TextField()
    emp_contribution = models.IntegerField()
    training_hours = models.IntegerField(null=True)
    application_status = models.CharField(null=True, default='pending',max_length=45)
    reason_for_denial = models.TextField(max_length=145, blank=True)
    total_cost = models.IntegerField(null=True)
    employee_contribution = models.TextField()
    employee_qualification = models.TextField()
    employee_signed = models.TextField()
    administrator_signed = models.TextField()
    evaluation = models.OneToOneField(Evaluation, null=True, blank=True, on_delete=models.CASCADE, related_name='training_application_record')

    class Meta:
        db_table = 'training_table'
    def __str__(self):
        return self.employee_name
    

class UserTraining(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='user_trainings')
    training = models.ForeignKey(TrainingApplications, on_delete=models.CASCADE)
    class Meta:
        db_table = 'user_training'
    def __str__(self):
        return f"{self.user} - {self.training}"