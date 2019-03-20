from django.http import HttpResponse
from django.shortcuts import render


def index(request):
    return HttpResponse('Hello, world!')


# home view
def home(request):
    return render(request, 'home.html', {})
