from django.shortcuts import render


# Create your views here.

def hello_world(request):
    name = 'Behshad RahmanPour'

    context = {'name':name}
    return render(request, 'src/index.html', context)