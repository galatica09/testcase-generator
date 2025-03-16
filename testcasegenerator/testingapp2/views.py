from django.http import JsonResponse

def about(request):
    return JsonResponse({"message": "Hello from app2!"})