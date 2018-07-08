from django.contrib import admin

from .models import *

# Register your models here.


class CategoryAdmin(admin.ModelAdmin):
    list_display = ('category_name', 'course', 'weight_percent')
    list_filter = ['course']


class StudentAdmin(admin.ModelAdmin):
    list_display = ('english_name', 'chinese_name')


class AssignmentAdmin(admin.ModelAdmin):
    list_display = ('assignment_name', 'course', 'category', 'total_points')
    list_filter = ['course']


class SubmissionAdmin(admin.ModelAdmin):
    list_display = ('assignment', 'grade', 'student')
    list_filter = ['assignment', 'student']


admin.site.register(Course)
admin.site.register(Student, StudentAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Assignment, AssignmentAdmin)
admin.site.register(Submission, SubmissionAdmin)
