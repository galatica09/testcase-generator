from django.http import JsonResponse

def home(request):
    return JsonResponse({"message": "Hello from app1!"})

def contact(request):
    return JsonResponse({"message": "Contact us!"})