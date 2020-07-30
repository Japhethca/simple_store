from django.shortcuts import render, HttpResponse

# Create your views here.
def test(request):
    return HttpResponse(b"this is a test for building application using docker")

