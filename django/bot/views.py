import json
import requests
from django.conf import settings
from django.shortcuts import render
from django.http import JsonResponse

RASA_URL = "http://rasa:5005/webhooks/rest/webhook"

# Create your views here.

def index(request):
    return render(request, "bot/index.html")

def handle_user_message(request):
    try:
        if (request.method != "POST"):
            return JsonResponse({"status":"error", "message" : "invalid method"}, status=405)
        
        data = json.loads(request.body)
        user_message = data.get("user_message")

        # GAURD CLAUSES
        if (not user_message):
            return JsonResponse({"status":"error", "message":"Empty message"}, status=400)
        if (user_message is None):
            return JsonResponse({"status":"error", "message":"user message is missing"}, status=400)
        if (not isinstance(user_message, str)):
            return JsonResponse({"status":"error", "message":"user message must be a string"}, status=400)
        if len(user_message) > 500:
            return JsonResponse({"status":"error","message":"Message too long"})
        
        print("======== user message =========", len(user_message))

        # FOR DEBUGGING ONLY
        # parse_response = requests.post("http://rasa:5005/model/parse", json={"text":user_message}).json()
        # print("=========parse result", parse_response["intent"], parse_response.get("entities"))
        
        # VERY IMPORTANT -> otherwise data will be fetched from cache
        sender_id = request.session.session_key
        if sender_id is None:
            request.session.create()
            sender_id = request.session.session_key

        # RESETTING TRACKER (only in development phase)
        # if (settings.APP_MODE=="development"):
        #     requests.post(f"http://rasa:5005/conversations/{sender_id}/tracker/events",json={"event": "restart"})

        # RASA REQUEST
        rasa_response = requests.post(RASA_URL, json={
            "sender": sender_id,
            "message": user_message
        })

        bot_message = rasa_response.json()
        bot_final_message = None

        print("========== bot msg ==========",bot_message[0])

        # REFACTORING BOT MESSAGE ON PURPOSE
        if bot_message and bot_message[0].get("buttons"):
            bot_final_message = {
                "sender":"bot",
                "sender_id":sender_id,
                "status":bot_message[0].get("status"),
                "text":bot_message[0].get("text"),
                "is_btn": True,
                "buttons":bot_message[0].get("buttons")
            }
        else:
            bot_final_message = {
                "sender":"bot",
                "sender_id": sender_id,
                "status":bot_message[0].get("status"),
                "text":bot_message[0].get("text"),
                "is_btn":False,
                "buttons":[]
                }

        return JsonResponse({"status": "success","response": bot_final_message})
    except Exception as e:
        print(e)
        return JsonResponse({"status":"error","message":"Internal server error"})