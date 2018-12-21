from .models import Teacher
from django import forms
from django.forms import ModelForm 
from django.contrib.auth import password_validation
from django.core.exceptions import ValidationError


#registration form
class TeachersRegistrationForm(ModelForm):
   

    confirm_password = forms.CharField(widget=forms.PasswordInput() , min_length=6 ,  help_text='Enter Your Password Again')
     
    class Meta:
        model = Teacher
        fields = ['teacher_email'  , 'password' , 'teacher_full_name',  'teacher_school_name']
       
    #check if email is not taken
    def clean_teacher_email(self):
        teacher_email = self.cleaned_data['teacher_email']
        if Teacher.objects.filter(teacher_email=teacher_email).exists():
            raise forms.ValidationError("A teacher with this email already exists. Sign in.")
        return teacher_email

    
    #make sure password and confirm password match
    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")

        if password != confirm_password:
            msg = "Passwords do not match"
            self.add_error('password', msg)
            self.add_error('confirm_password', msg)

        try:
            password_validation.validate_password(password,Teacher,password_validation.get_default_password_validators())
        except ValidationError as password_errors:
            self.add_error('password',password_errors)

    #set the email and password
    def save(self, commit=True):
        teacher = super().save(commit=False)
        teacher.set_password(self.cleaned_data['password'])
        teacher.set_teacher_email(self.cleaned_data['teacher_email'])
        if commit:
            teacher.save()
        return teacher

        
        
#login form
class TeachersLoginForm(forms.Form):
    teacher_email = forms.CharField(widget=forms.EmailInput() , required = True , label = 'Email' , help_text='Your Email')
    password = forms.CharField(widget=forms.PasswordInput() , required = True , label='Password' , help_text='Your Password')
   
   