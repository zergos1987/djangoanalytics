from django.shortcuts import render, redirect



# Create your views here.
def index(request):

	template = 'app_zs_admin/index.html'

	return render(request, template)