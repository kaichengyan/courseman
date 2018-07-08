from django.db import models

# Create your models here.


class Course(models.Model):
    subject_code = models.CharField(max_length=3)
    course_num = models.IntegerField()
    course_name = models.CharField(max_length=50)

    def __str__(self):
        return self.subject_code + " " + str(self.course_num)


class Student(models.Model):
    english_name = models.CharField(max_length=30)
    chinese_name = models.CharField(max_length=30)
    course = models.ManyToManyField(Course)

    def __str__(self):
        return self.english_name + ' (' + self.chinese_name + ')'

    class Meta:
        ordering = ('english_name', )


class Category(models.Model):
    category_name = models.CharField(max_length=50)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    weight_percent = models.IntegerField()

    def __str__(self):
        return self.category_name + ' (' + str(self.course) + ')'


class Assignment(models.Model):
    assignment_name = models.CharField(max_length=50)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    total_points = models.IntegerField()

    def __str__(self):
        return self.assignment_name + ' (' + str(self.course) + ')'

    class Meta:
        ordering = ('category', )


class Submission(models.Model):
    assignment = models.ForeignKey(Assignment, on_delete=models.CASCADE)
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    grade = models.IntegerField()

    def __str__(self):
        return str(self.student) + '\'s ' + str(self.assignment)

    class Meta:
        ordering = ('assignment__category__course', 'assignment__category', '-grade', 'student')
