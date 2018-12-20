from django.db import models
from django.utils.timezone import now , localdate
from django.contrib.auth.models import PermissionsMixin
from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from django.template.defaultfilters import slugify

# Create your models here.

#the manager for Teachers model class -- see below 
class TeacherManager(BaseUserManager):
    def create_teacher(self,  teacher_full_name ,   teacher_email ,  password , teacher_school_name):
        if not teacher_email:
            raise ValueError('teachers must provide their email id')
        teacher = self.model( teacher_email = teacher_email, 
        teacher_full_name = teacher_full_name,
        teacher_school_name = teacher_school_name ,  
        password = password)  
        teacher.set_password(password)
        teacher.save(using=self._db)
        return teacher

    def create_superuser(self,teacher_full_name ,   teacher_email ,  password , teacher_school_name = None ):
       
        teacher = self.create_teacher(
            teacher_email = teacher_email, 
            teacher_full_name = teacher_full_name,
            teacher_school_name = teacher_school_name ,  
            password = password
            )
        teacher.is_superuser = True
        teacher.is_staff = True
        teacher.is_active = True
        teacher.save(using=self._db)
        return teacher




#the custom class for wordgame teachers
class Teacher(AbstractBaseUser , PermissionsMixin):

    #the fields 
    teacher_full_name = models.CharField( db_column = 'Full Name' , max_length=64)
    teacher_school_name = models.CharField(db_column = 'School Name', max_length=128, null = True )
    teacher_email = models.EmailField(db_column = 'Email Address' , unique=True , db_index = True)
   
    is_active = models.BooleanField(default=True) 
    is_staff = models.BooleanField(default=False)
    is_superuser =  models.BooleanField(default=False)
    date_joined = models.DateTimeField(default=now)


    USERNAME_FIELD = 'teacher_email'
    EMAIL_FIELD = 'teacher_email'

    
    REQUIRED_FIELDS = ['teacher_full_name']

    objects = TeacherManager()

    class Meta():
        ordering = ('-date_joined', )
       

    def get_full_name(self):
        return self.teacher_full_name

    def get_short_name(self):
        return str(self.teacher_full_name).split()[0]
    
    def __str__(self):
        return self.teacher_full_name

    def set_teacher_email(self,teacher_email):
        self.teacher_email = teacher_email



#english words used throughout the site
class Words(models.Model):
    eng_word = models.CharField(max_length = 64 , help_text = 'Word in english'  )
    chinese_word = models.TextField( help_text = 'chinese translation'  )
    pinyin_word = models.TextField(help_text = 'pinyin translation'  )
    pronunciation_ipa = models.CharField(max_length = 96   )
    word_audio = models.FileField(upload_to="EnglishWords", help_text="upload the audio for pronunciation")
    
    class Meta:
        verbose_name_plural = "Words"