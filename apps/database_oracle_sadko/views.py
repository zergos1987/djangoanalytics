from django.shortcuts import render, redirect



# Create your views here.
def index(request):

	template = 'database_oracle_sadko/index.html'

	return render(request, template)