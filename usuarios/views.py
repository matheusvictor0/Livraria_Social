
from django.shortcuts import render
from django.http import HttpResponse


#deflogin(request):
    #return HttpResponse('login')


def cadastro(request):
    return render(request, 'cadastro.html')
