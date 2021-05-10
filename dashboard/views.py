from django.shortcuts import render, reverse
from django.http import HttpResponse

def home(request):
	return HttpResponse("Hello world")
