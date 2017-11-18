import ask_app.models as m

for i in range(1, 20):
    my_username='username ' + str(i)
    my_email='email ' + str(i)
    my_password='password ' + str(i)
    user = UserProfile(username=my_username, password=my_password, email=my_email)
    user.save()

for i in range(1, 30):
    my_title='title ' + str(i)
    my_text='text ' + str(i)
    my_author=str(i%20)
    #my_create_date = now()
    question = Question(title=my_title, text=my_text, author=my_author)
    question.save()



