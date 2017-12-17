# coding=utf-8
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib.auth import authenticate, login as l_in, logout as l_out
from django.http import HttpResponseRedirect

from ask_app import forms
from .models import *

def settings(request):
    return render(request, 'settings.html')


def login(request):
    return render(request, 'login.html')


def registration(request):
    return render(request, 'registration.html')


def index(request):
    questions = Question.objects.recent_questions()
    questions_for_render = paginate(questions, request)
    return render(request, 'index.html', {
        'objects': questions_for_render,
    })


#def indexlog(request):
#    questions = Question.objects.all()
#    questions_for_render = paginate(questions, request)
#    return render(request, 'indexlog.html', {
#        'objects': questions_for_render,
#    })


def tag(request, name):
    questions = Question.objects.questions_by_tag(name)
    questions_for_render = paginate(questions, request)
    return render(request, 'tag.html', {
        'objects': questions_for_render,
    })


def hot(request):
    questions = Question.objects.questions_with_high_rating()
    questions_for_render = paginate(questions, request)
    return render(request, 'index.html', {
        'objects': questions_for_render,
    })


def question(request, id):
    main_question = Question.objects.get_with_tags(id)
    answers = Answer.objects.get_with_likes(id)
    answers_for_render = paginate(answers, request)
    context = {'question': main_question, 'answers': answers_for_render}
    return render(request, 'question.html', context)


def ask(request):
    return render(request, 'ask.html')


def paginate(objects_list, request, page_objects_num=20):
    paginator = Paginator(objects_list, page_objects_num)
    page = request.GET.get('page')

    try:
        objects_page = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        objects_page = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        objects_page = paginator.page(paginator.num_pages)
    return objects_page

def _get_user_context(request):
    context = {}
    if request.user.is_authenticated():
        context['user_logged_in'] = True
        context['username'] = request.user.username
    else:
        context['user_logged_in'] = False
    return context

def register(request):
    context = _get_user_context(request)
    errors = []
    if context['user_logged_in']:
        return HttpResponseRedirect('/')
    if request.method == 'POST':
        form = forms.RegistrationForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            email = form.cleaned_data['email']
            firstname = form.cleaned_data['firstname']
            lastname = form.cleaned_data['lastname']
            password = form.cleaned_data['password']
            confirmpass = form.cleaned_data['confirmpass']
            if password != confirmpass:
                errors.append("Пароли не совпадают")
            data = form.data.copy()
            same = None
            try:
                same = UserProfile.objects.get(username=username)
            except UserProfile.DoesNotExist:
                pass
            if same:
                errors.append("Пользователь с таким именем уже существует")
                data['username'] = ""
            same = None
            try:
                same = UserProfile.objects.get(email=email)
            except UserProfile.DoesNotExist:
                pass
            if same:
                errors.append("Пользователь с таким адресом эл. почты уже существует")
                data['email'] = ""
            form.data = data
            if errors:
                return render(request, 'register.html', {'form': form,
                              'errors': errors})
            UserProfile.objects.create_user(username=username, email=email, password=password, first_name=firstname, last_name=lastname)
        return HttpResponseRedirect("/login/")
    return render(request, 'register.html', {'form': forms.RegistrationForm(), 'errors': []})

def login(request):
    context = _get_user_context(request)
    errors = []
    if context["user_logged_in"]:
        return HttpResponseRedirect('/')
    if request.method == 'POST':
        form = forms.LoginForm(request.POST)
        if form.is_valid():
            username_or_email = form.cleaned_data['username_or_email']
            password = form.cleaned_data['password']
            user = None
            try:
                user = UserProfile.objects.get(username=username_or_email)
            except UserProfile.DoesNotExist:
                try:
                    user = UserProfile.objects.get(email=username_or_email)
                except UserProfile.DoesNotExist:
                    errors.append("Пользователя с таким именем или адресом эл. почты не существует")
                    return render(request, 'login.html', {'form': form, 'errors': errors})
            user_auth = authenticate(username=user.username, password=password)
            if user_auth is not None:
                l_in(request, user_auth)
                return HttpResponseRedirect("/success/")
            else:
                errors.append("Пароль неверен")
                return render(request, 'login.html', {'form': form, 'errors': errors})
    return render(request, 'login.html', {'form': forms.LoginForm()})

def success(request):
    context = _get_user_context(request)
    if request.user.is_authenticated():
        context['success'] = True
        return render(request, 'success.html', context)
    else:
        return render(request, 'success.html', {"success": False})

def logout(request):
    if request.user.is_authenticated():
        l_out(request)
        return HttpResponseRedirect('/login/')
    else:
        return HttpResponseRedirect('/')