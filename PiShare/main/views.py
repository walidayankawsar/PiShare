from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse, HttpResponse
from .models import Session
from .forms import FileForm
import qrcode
from django.conf import settings


# Create your views here.




def cleanup():
    for s in Session.objects.all():
        s.cleanup()   #model er cleanup method ke call korche

def home(request):
    cleanup()
    return render(request, 'index.html')
