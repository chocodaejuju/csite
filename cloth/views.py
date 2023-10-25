from django.http import HttpResponse
from django.shortcuts import render, redirect

def index(request):
    return render(request, 'main/first.html')
# Create your views here.
