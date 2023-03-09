from django.shortcuts import render
from .tasks import notification_customer

# Create your views here.


def home(request):
    notification_customer.delay('Hello i am Behshad')
    return render(request, 'src/main.html')
