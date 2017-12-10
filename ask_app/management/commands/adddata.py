# -*- coding: utf-8 -*-
from django.core.management.base import BaseCommand, CommandError
from django.contrib.auth.models import UserManager
from ask_app.models import *
from faker import Faker


class ManagerUserProfile:
    def create_user(self, username, password, email):
        if not email:
            raise ValueError('Users must have an email address')
        if not username:
            raise ValueError('Users must have a username')
        if not password:
            raise ValueError('Users must have a password')

        user = UserProfile(username=username, email=email, password=password)
        user.save()
        return user

    def get_by_username(self, username):
        user = UserProfile.objects.get(username=username)
        return user

    def get_by_id(self, _id):
        user = UserProfile.objects.get(id=_id)
        return user

fake = Faker()
usermanager = ManagerUserProfile()


def create_user():
    name = fake.name()
    email = fake.email()
    passwrd = fake.password()
    usermanager.create_user(username=name, password=passwrd, email=email)
    print('Successfully fill data for user "%s", "%s", "%s"' % (name, email, passwrd))

def create_question(user_id):
    title = fake.sentence()
    text = fake.text()
    question = Question(title=title, text=text, author=usermanager.get_by_id(user_id))
    question.save()
    print('Successfully fill data for question "%s", "%d"' % (title, user_id))

def create_answer(question_id, user_id):
    text = fake.sentence()
    answer1 = Answer(text=text, author=usermanager.get_by_id(user_id), question=Question.objects.get(id=question_id))
    answer1.save()
    answer2 = Answer(text=text, author=usermanager.get_by_id(user_id), question=Question.objects.get(id=question_id % 5))
    answer2.save()
    print('Successfully fill data for answer1 "%d", "%d"' % (question_id, user_id))
    print('Successfully fill data for answer2 "%d", "%d"' % (question_id % 5, user_id))

def create_tag(question_id):
    name_tag = fake.words()[0]
    tag = Tag()
    tag.name = name_tag
    tag.save()
    tag.questions.add(Question.objects.get(id=question_id))
    tag.questions.add(Question.objects.get(id=question_id + 3))
    tag.save()
    print('Successfully fill data for tag "%s", "%d", "%d"' % (name_tag, question_id, question_id + 3))

def create_like_answer(answer_id, user_id):
    like_answer = LikeAnswer(like_target_answer=Answer.objects.get(id=answer_id), author=usermanager.get_by_id(user_id))
    like_answer.save();
    print('Successfully fill data for like_answer "%d", "%d"' % (answer_id, user_id))

def create_like_question(question_id, user_id):
    like_question = LikeQuestion(like_target_question=Question.objects.get(id=question_id), author=usermanager.get_by_id(user_id))
    like_question.save();
    print('Successfully fill data for like_question "%d", "%d"' % (question_id, user_id))

class Command(BaseCommand):
    def handle(self, *args, **options):
        max_const = 100
        #for i in range(1, max_const):
        #    create_user()

        #for i in range(1, max_const):
        #    create_question(i)

        #for i in range(1, max_const):
        #    create_answer(i, i)

        #for i in range(1, max_const):
        #    create_tag(i)

        for i in range(1, max_const):
            create_like_answer(i%10 + 20, i%50 + 1)
            create_like_question(i%10 + 20, i%50 + 1)