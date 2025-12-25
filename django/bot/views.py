from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
import requests
import json

RASA_URL = "http://rasa:5005/webhooks/rest/webhook"

# Create your views here.

@csrf_exempt
def chat(request):
    if request.method != "POST":
        return JsonResponse({"error": "POST request required"}, status=400)

    data = json.loads(request.body)
    message = data.get("message")
    sender = data.get("sender", "default")

    payload = {
        "sender": sender,
        "message": message
    }

    response = requests.post(RASA_URL, json=payload)
    print("RASA response:", response)
    return JsonResponse(response.json(), safe=False)

def index(request):
    return render(request, "bot/index.html")

def handle_user_message(requset):
    data = json.loads(requset.body)

    user_message = data.get("user_message")

    print("User message:", user_message)

    
    rasa_response = requests.post(RASA_URL, json={
        "sender": "user",
        "message": user_message
    })

    bot_message = rasa_response.json()

    return JsonResponse({"status": "success"," response": bot_message})