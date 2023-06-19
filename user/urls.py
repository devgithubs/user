from django.urls import path
from . import views

app_name = "user"

urlpatterns = [
    path('', views.index, name='index'),
    # Training Course Application urls
    path('course_application/', views.course_application, name='course_application'),
    path('course_application_list/', views.course_application_list, name='course_application_list'),
    path('employee_course_application_list/', views.employee_course_application_list, name='employee_course_application_list'),
    path('application/<int:application_id>/', views.application_detail, name='application_detail'),
    path('employee_application_detail/<int:application_id>/', views.employee_application_detail, name='employee_application_detail'),
    path('application/<int:application_id>/approve/', views.approve_application, name='approve_application'),
    path('application/<int:application_id>/deny/', views.deny_application, name='deny_application'),
    path('application/<int:application_id>/edit/', views.edit_application, name='edit_application'),
    path('application/<int:application_id>/delete/', views.delete_application, name='delete_application'),
    # Evaluation
    path('evaluation/list/', views.evaluation_list, name='evaluation_list'),
    path('evaluation/form/<int:pk>/', views.evaluation_form, name='evaluation_form'),
    #
    #
    # path('evaluation_detail/<int:id>/', views.evaluation_detail, name='evaluation_detail'),
    # path('evaluation_list/', views.evaluation_list, name='evaluation_list'),
    # path('create_evaluation/', views.create_evaluation, name='create_evaluation'),
    path('generate_report/<int:employee_id>/', views.generate_report, name='generate_report'),
    path('download_csv/<int:employee_id>/', views.download_csv, name='download_csv'),
    path('register/', views.register_view, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('search_employee/', views.search_employee, name='search_employee'),
    path('employee_list/', views.employee_list, name='employee_list'),
    path('inactive_employees/', views.inactive_employees, name='inactive_employees'),
    path('password-reset/', views.password_reset_view, name='password_reset'),
]
