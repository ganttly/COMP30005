# Create your views here.
from django.http import HttpResponse

def idnex(request):
	return HttpResponse("Hello, world.")