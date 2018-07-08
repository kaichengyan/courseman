from django.shortcuts import render, get_object_or_404, redirect
from django.db.models import Avg
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect

from .forms import LoginForm
from .models import Course, Student, Assignment, Category, Submission


# Create your views here.


def view_courses(request):
    course_list = Course.objects.all()
    context = {
        'course_list': course_list
    }
    return render(request, 'course/index.html', context)


@login_required
def view_students(request):
    student_list = Student.objects.all()
    context = {
        'student_list': student_list
    }
    return render(request, 'student/index.html', context)


def course_detail(request, course_id):
    course = get_object_or_404(Course, pk=course_id)
    return render(request, 'course/detail.html', {'course': course})


@login_required
def course_students(request, course_id):
    course = get_object_or_404(Course, pk=course_id)
    students = Student.objects.filter(course=course_id)
    return render(request, 'course/students.html', {
        'student_list': students,
        'course': course
    })


def course_assignments(request, course_id):
    course = get_object_or_404(Course, pk=course_id)
    assignments = Assignment.objects.filter(
        course=course_id).order_by('category')
    return render(request, 'course/assignments.html', {
        'assignment_list': assignments,
        'course': course
    })


@login_required
def student_detail(request, student_id):
    student = get_object_or_404(Student, pk=student_id)
    courses = Course.objects.filter(student=student_id)
    return render(request, 'student/detail.html', {
        'student': student,
        'courses': courses
    })


@login_required
def student_detail_by_course(request, course_id, student_id):
    course = get_object_or_404(Course, pk=course_id)
    student = get_object_or_404(Student, pk=student_id)
    submissions = Submission.objects.filter(student=student_id)
    categories = Category.objects.filter(course=course_id)
    grades_for_categories = {}
    for c in categories:
        grades_for_categories[c] = []
    for s in submissions:
        grade_percent = s.grade / s.assignment.total_points
        grades_for_categories[s.assignment.category].append(grade_percent)
    predicted_grade = 0
    for c in categories:
        if grades_for_categories[c]:
            predicted_grade += c.weight_percent / 100.0 * \
                (sum(grades_for_categories[c]) / len(grades_for_categories[c]))
        else:
            predicted_grade += c.weight_percent / 100.0 * 1
    predicted_grade *= 100
    return render(request, 'course/student_detail.html', {
        'student': student,
        'course': course,
        'submissions': submissions,
        'predicted_grade': predicted_grade
    })


@login_required
def assignment_detail(request, course_id, assignment_id):
    course = get_object_or_404(Course, pk=course_id)
    assignment = get_object_or_404(Assignment, pk=assignment_id)
    submissions = Submission.objects.filter(assignment=assignment_id)
    average = submissions.aggregate(Avg('grade'))['grade__avg']
    return render(request, 'assignment/detail.html', {
        'assignment': assignment,
        'course': course,
        'submissions': submissions,
        'average': average
    })


def login_view(request):
    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                if 'next' in request.POST:
                    return redirect(request.POST['next'])
                else:
                    return redirect('/')
    else:
        form = LoginForm()
    return render(request, 'accounts/login.html', {"form": form})


@login_required
def logout_view(request):
    logout(request)
    return redirect('/')
