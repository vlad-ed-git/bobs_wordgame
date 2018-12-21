from django.db import models
from wordgameweb.models import Teacher
from django.utils.timezone import now 

# Create your models here.
#the model class for wordgame students
class Student(models.Model):

    #the fields 
    student_full_name = models.CharField( db_column = 'Full Name' , max_length=64)
    students_teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE)
    student_reg_no = models.CharField( db_column = 'Registration Number' , max_length=64)
    student_password = models.CharField( db_column = 'Password' , max_length=255)
    date_joined = models.DateTimeField(default=now)

    class Meta():
        ordering = ('-date_joined', )
        unique_together = ('student_reg_no', 'students_teacher')