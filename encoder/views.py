from django.shortcuts import render
from django.http import HttpResponse
def index(request):
    return render(request,'encoder/home.html')
def encode(request):
    return render(request,'encoder/encode.html')
def decode(request):
    return render(request,'encoder/decode.html')