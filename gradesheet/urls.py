from django.urls import path

from . import views

urlpatterns = [
    path('', views.view_courses, name='index'),
    path('courses/', views.view_courses, name='view_courses'),
    path('students/', views.view_students, name='view_students'),
    path('course/<int:course_id>/', views.course_detail, name='course_detail'),
    path('course/<int:course_id>/students/',
         views.course_students, name='course_students'),
    path('course/<int:course_id>/student/<int:student_id>/',
         views.student_detail_by_course, name='student_detail_by_course'),
    path('student/<int:student_id>/',
         views.student_detail, name='student_detail'),
    path('course/<int:course_id>/assignments/',
         views.course_assignments, name='course_assignments'),
    path('course/<int:course_id>/assignment/<int:assignment_id>/',
         views.assignment_detail, name='assignment_detail'),
    path('accounts/login/', views.login_view, name='login_view'),
    path('accounts/logout/', views.logout_view, name='logout_view'),
]
