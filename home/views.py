from django.shortcuts import render
from django.core.mail import send_mail, BadHeaderError

# Create your views here.

def home(request):
    # Send mail
    # try:
    #     send_mail(
    #         'hello world', 
    #         'send mail is successful', 
    #         'behshad.rahmanpour@gmail.com', 
    #         ['roino@gmail.com']
    #     )
    # except BadHeaderError:
    #     pass

    return render(request, 'src/main.html')
