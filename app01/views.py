from django.shortcuts import render

# Create your views here.

def index(request):

    return render(request,'index.html')

def news(request):

    return render(request,'news.html')

def login(request):
    return render(request, 'login.html')

def sign(request):
    return render(request, 'sign.html')
