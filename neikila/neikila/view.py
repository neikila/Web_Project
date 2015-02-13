from django.http import HttpResponse
import datetime

def hello(request):
    Hello = "Hello World1"
    return HttpResponse(Hello)
