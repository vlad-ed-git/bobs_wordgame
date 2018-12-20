from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth import forms
from .models import Teacher , Words

#forms for admin dashboard
class BobTeacherChangeForm(forms.UserChangeForm):
   

    class Meta:
        model = Teacher
        fields = ( 'teacher_full_name' ,   'teacher_email' ,  'password' , 'teacher_school_name' ,  'is_active')
        field_classes = {'username': Teacher.USERNAME_FIELD}

class BobTeacherCreationForm(forms.UserCreationForm):
    
    class Meta:
        model = Teacher
        fields = ( 'teacher_full_name' ,   'teacher_email' ,  'teacher_school_name' )
        field_classes = {'username': Teacher.USERNAME_FIELD}

  


#my custom teacher admin
class BobTeacherAdmin(UserAdmin):
    fieldsets = (
        (None, {'fields': ('teacher_email', 'password')}),
        ('Personal info', {'fields': ( 'teacher_full_name' ,   'teacher_school_name' )}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser',
                                       'groups', 'user_permissions')}),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('teacher_email', 'password1', 'password2'),
        }),
    )
    form = BobTeacherChangeForm
    add_form = BobTeacherCreationForm
    list_display = ('teacher_full_name' , 'teacher_email', )
    list_filter = (  'is_active', 'is_staff')
    search_fields = ('teacher_email',)
    ordering = ('date_joined',)
    filter_horizontal = ()


# Register your models here.
admin.site.register(Teacher, BobTeacherAdmin)
admin.site.register(Words)