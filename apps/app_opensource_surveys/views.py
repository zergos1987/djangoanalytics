from django.shortcuts import render, redirect



# Create your views here.
def index(request):

	template = 'app_opensource_surveys/index.html'

	return render(request, template)