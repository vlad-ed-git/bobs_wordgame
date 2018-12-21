from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from wordgameweb.forms import TeachersLoginForm,  TeachersRegistrationForm
from .models import Teacher, TeachersList, Words
from django.urls import reverse
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout
from django.core.exceptions import ValidationError
from django import forms
from wordgameapi.models import Student

# Create your views here.
def signIn(request):
    #if teacher has already logged in, send them home
    if request.user.is_authenticated:
        return home(request)
    
    
    # variable to assign has errors class
    has_errors = 'has_errors'

    # if teacher signed up and submitted form
    if request.method == "POST" and 'sign_up_btn' in request.POST:
        # teacher is signing up
        sign_up_form = TeachersRegistrationForm(request.POST)
        # sign in form must be initialized too
        sign_in_form = TeachersLoginForm()

        # validating
        try:
            if sign_up_form.is_valid():
                new_teacher = sign_up_form.save()
                new_teacher = authenticate(request, username=sign_up_form.cleaned_data['teacher_email'],
                                        password=sign_up_form.cleaned_data['password'])
                if new_teacher is not None:
                    login(request, new_teacher)  # login this teacher
                    return render(request, 'wordgameweb/home.html')
        except ValidationError as non_field_errors:
            sign_up_form.add_error('teacher_full_name', non_field_errors)
        except:
            sign_up_form.add_error('teacher_full_name', "please provide valid information")

    
    # if teacher signed in and submitted form
    elif request.method == "POST" and 'sign_in_btn' in request.POST:
        # teacher is signing in
        sign_in_form = TeachersLoginForm(request.POST)
        # sign up form must be initialized too incase an error occurs and we stay in login page
        sign_up_form = TeachersRegistrationForm()

       
        teacher_email = request.POST['teacher_email']
        password = request.POST['password']
        old_teacher = authenticate(request, teacher_email=teacher_email, password=password)
        if old_teacher is not None:
            login(request, old_teacher)  # login this teacher
            # send teacher back to their page
            return render(request, 'wordgameweb/home.html')
        else:
            sign_in_form.add_error('password', forms.ValidationError("Incorrect email or password!"))


    else:
        # teacher is viewing the forms at first . no submission yet
        sign_up_form = TeachersRegistrationForm()
        sign_in_form = TeachersLoginForm()

    # if teacher is just viewing login page ( or submitted either form but with errors)
    return render(request, 'wordgameweb/login.html',
                  {'sign_up_form': sign_up_form, 'sign_in_form': sign_in_form, 'has_errors': has_errors})




#takes teacher to home page, if they are logged in
@login_required
def home(request):
    if request.method == "POST" and 'deleteListBtn' in request.POST:
        list_number  = request.POST['list_no']
        try:
            list_no = int(list_number)
            TeachersList.objects.filter(created_by = request.user , list_number = list_no).delete()
        except Exception:
            pass
        

    #get this teachers students
    my_students = Student.objects.filter(students_teacher = request.user )

    #get this teachers lists
    my_lists = TeachersList.objects.filter(created_by = request.user)
    #list numbers will be duplicated , remove duplicates
    final_list_numbers = [] 
    for my_list in my_lists:
        if my_list.list_number not in final_list_numbers: 
            final_list_numbers.append(my_list.list_number)
    return render(request, 'wordgameweb/home.html' , { 'my_students' : my_students , 'my_lists' : final_list_numbers})


#takes teacher to create list
def create_list(request):
    #get count of words
    totalWordsCurrentlyInDb = Words.objects.count()

    #if user clicked done
    if request.method == "POST" and 'doneListBtn' in request.POST:
        #get the list number and selected words       
        checked_words = request.POST.getlist('eng_words_checker')
        if len(checked_words) > 0 or len(request.session['selected_word_ids']):
            request.session['selected_word_ids'].extend(checked_words)
            request.session.modified = True
            list_number = request.POST['list_number_input']
            
            #save in db
            try:
                for selected_word_id in request.session['selected_word_ids']:
                    selected_word = Words.objects.get(id=selected_word_id)
                    new_list = TeachersList(list_number = list_number , created_by = request.user , words = selected_word)
                    new_list.save()
            except Exception:
                pass
            
            
            #clearing session
            del request.session['selected_word_ids']

            #going home
            return home(request)

    #user clicked a number to jump to
    elif request.method == "POST" and 'jumpListBtn' in request.POST:
        checked_words = request.POST.getlist('eng_words_checker')
        if len(checked_words) > 0:
            request.session['selected_word_ids'].extend(checked_words)
            request.session.modified = True
        offset = int(request.POST['jumpListBtn'])
        print(offset) 
    
    elif request.method == "POST" and 'prevListBtn' in request.POST:
        checked_words = request.POST.getlist('eng_words_checker')
        if len(checked_words) > 0:
            request.session['selected_word_ids'].extend(checked_words)
            request.session.modified = True
        offset = int(request.POST['prevListBtn']) - 45
        
    elif request.method == "POST" and 'nextListBtn' in request.POST:
        checked_words = request.POST.getlist('eng_words_checker')
        if len(checked_words) > 0:
            request.session['selected_word_ids'].extend(checked_words)
            request.session.modified = True
        offset = int(request.POST['nextListBtn'])

    else:
        #we are fetching the very first batch
        #deleted any previously stored words in session
        if request.session.get('selected_word_ids', False):
            del request.session['selected_word_ids']

        request.session['selected_word_ids'] = []

        offset = 0


    #gets 45 words at a time
    limit = offset + 45
    words_batch = Words.objects.order_by('eng_word')[offset:limit]
    batch1 = []
    batch2 = []
    batch3 = []
    results = 0
    for counter , word in enumerate(words_batch):
        if counter < 15:
            batch1.append(word)
        elif counter < 30:
            batch2.append(word)
        else:
            batch3.append(word)
        results = results + 1
    

    #if we have a next batch
    if results < 45:
        limit = 0

    i = 0
    batches = []
    while i < totalWordsCurrentlyInDb:
        batches.append(i)
        i =  i + 135
    return render(request, 'wordgameweb/choose_english_words.html' , {'batch1' : batch1 , 'batch2' : batch2 , 'batch3' : batch3, 'prev_start' : offset , 'next_start' : limit , 'batch_intervals' : batches} )



@login_required
def signOut(request):
    logout(request)
    return signIn(request)



@login_required
def editList(request , list_number):
    if request.method == "POST" and 'deleteWordsBtn' in request.POST:
        list_ids = request.POST.getlist('word_checker')
        try:

            for list_id in list_ids:
                    list_id = int(list_id)
                    TeachersList.objects.filter(id=list_id).delete()
        except Exception:
            pass
 
    #get all words of this list
    teachers_list = TeachersList.objects.filter(list_number = list_number, created_by  = request.user ) 
    return render(request, 'wordgameweb/list.html', {'teachers_list' : teachers_list , 'list_number' : list_number , 'list_created_on' : teachers_list[0].date_created })

@login_required
def viewWord(request , word_id, list_number ):
    #get all words of this list
    word = Words.objects.get( id = word_id) 
    return render(request, 'wordgameweb/word.html', {'word' : word , 'list_number':list_number })
