from django.shortcuts import render
from django.http import HttpResponse
# Create your views here.

from djobs.models import *
def index(request):
    context = {"list":DJobItem.objects.all()}
    return render(request,'mydjob/index.html',context)