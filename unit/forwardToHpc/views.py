from django.shortcuts import render, HttpResponse
import requests


# Create your views here.
def forwardtohpc(request):
    url = "http://192.168.191.218:8000/ceshi/index/"
    return HttpResponse(requests.get(url))
