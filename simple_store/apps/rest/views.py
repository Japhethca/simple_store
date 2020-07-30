from django.http.response import JsonResponse

# Create your views here.


def test_api(request):
    return JsonResponse({"message": "this is a test api"})

