from django.http import HttpRequest, HttpResponse
from django.shortcuts import render
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
import collections

from .models import *
"""
    questions = Questions.objects.all_with_tags()
    
    //all_with_tags:
        questions = list(Questions.objects.all())
    for q in questions:
        tags = list(Tag.objects.filter(question=q))
        q.tags = tags
        return questions;
    
    """

def settings(request):
    return render(request, 'settings.html')


def login(request):
    return render(request, 'login.html')


def registration(request):
    return render(request, 'registration.html')


def index(request):
    #questions = Question.objects.all()
    #questions = Question.objects.get_all_with_tags()
    questions = Question.objects.recent_questions()
    questions_for_render = paginate(questions, request)
    return render(request, 'index.html', {
        'objects': questions_for_render,
    })


def indexlog(request):
    questions = Question.objects.all()
    questions_for_render = paginate(questions, request)
    return render(request, 'indexlog.html', {
        'objects': questions_for_render,
    })


def tag(request, name):
    questions = Question.objects.questions_with_tag(name)
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
    answers = Answer.objects.filter(question=int(id))
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
