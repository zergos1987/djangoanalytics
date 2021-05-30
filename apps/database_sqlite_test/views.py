from django.shortcuts import render, redirect



# Create your views here.
def index(request):

	template = 'database_sqlite_test/index.html'

	return render(request, template)