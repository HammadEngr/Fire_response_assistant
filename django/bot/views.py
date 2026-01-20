import json
import requests
from django.conf import settings
from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import logging

logger = logging.getLogger(__name__)

RASA_URL = "http://rasa:5005/webhooks/rest/webhook"

# Create your views here.
@csrf_exempt
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

        logger.info(f"Sending to Rasa - Sender: {sender_id}, Message: {user_message}")
        parse_response = requests.post("http://rasa:5005/model/parse", json={"text": user_message}).json()
        logger.info(f"Parse result - Intent: {parse_response.get('intent')}, Entities: {parse_response.get('entities')}")


        # RASA REQUEST
        rasa_response = requests.post(RASA_URL, json={
            "sender": sender_id,
            "message": user_message
        })

        if rasa_response.status_code != 200:
            return JsonResponse({
            "status": "error",
            "message": "Assistant service unavailable"
        }, status=503)

        logger.info(f"rasa====={rasa_response}")

        bot_message = rasa_response.json()
        logger.info(f"bot_message---{bot_message}")

        if not bot_message or not isinstance(bot_message, list):
            return JsonResponse({
                "status": "error",
                "message": "No response from assistant"
            }, status=502)

        all_messages = []

        for msg in bot_message:
            if msg.get("custom"):
                custom_data = msg["custom"]
                all_messages.append({
                    "sender": "bot",
                    "sender_id": sender_id,
                    "message_type": "custom",
                    "data": custom_data,
                    "text": custom_data.get("heading", "Emergency Instructions"),
                    "is_btn": False,
                    "buttons": []
                })

            elif msg.get("buttons"):
                all_messages.append({
                    "sender": "bot",
                    "sender_id": sender_id,
                    "message_type": "buttons",
                    "text": msg.get("text", ""),
                    "is_btn": True,
                    "buttons": msg.get("buttons")
                })

            else:
                all_messages.append({
                    "sender": "bot",
                    "sender_id": sender_id,
                    "message_type": "text",
                    "text": msg.get("text", ""),
                    "is_btn": False,
                    "buttons": []
                })

        logger.info(all_messages)

        return JsonResponse({"status": "success", "response": all_messages})
    except Exception as e:
        print(e)
        return JsonResponse({"status":"error","message":str(e)})