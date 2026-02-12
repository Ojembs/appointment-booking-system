from django.shortcuts import render
from urllib import request

# Create your views here.
def index(request):
    context = {}
    return render(request, '', context)