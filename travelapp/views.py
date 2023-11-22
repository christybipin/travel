from django.http import HttpResponse
from django.shortcuts import render

from travelapp.models import movie

def about(request):
    obj = movie.objects.all()
    return render(request, 'index.html',{'result':obj})

