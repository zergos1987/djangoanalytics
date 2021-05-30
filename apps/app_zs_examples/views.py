from django.shortcuts import render, redirect



# Create your views here.
def index(request):

	template = 'app_zs_examples/index.html'

	return render(request, template)