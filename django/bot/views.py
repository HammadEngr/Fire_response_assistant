import json
import requests
from django.conf import settings
from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils import timezone
from .models import UserSubmission
import logging

from geopy.geocoders import Nominatim

def get_address(lat, lng):
    geolocator = Nominatim(user_agent="fire_crisis_bot")
    location = geolocator.reverse(f"{lat}, {lng}")
    return location.address if location else None

logger = logging.getLogger(__name__)

RASA_URL = "http://rasa:5005/webhooks/rest/webhook"

@csrf_exempt
def index(request):
    return render(request, "bot/index.html")

def get_save_location(request):
    if request.method == "POST":
        data = json.loads(request.body)
        latitude = data.get("latitude")
        longitude = data.get("longitude")
        sender_id = request.session.session_key
        
        address = get_address(latitude, longitude)

        submission, created = UserSubmission.objects.update_or_create(
            user_id=sender_id,
            defaults={          
                "latitude": latitude,
                "longitude": longitude,
                "description": "Location submission",
                "resolved_address": address,
            }
        )
        action = "created" if created else "updated"
        return JsonResponse({"status": "success", "message": f"Location {action}"})
    else:
        return JsonResponse({"status": "error", "message": "Invalid request method"}, status=400)

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
        
        # VERY IMPORTANT -> otherwise data will be fetched from cache
        sender_id = request.session.session_key
        if sender_id is None:
            request.session.create()
            sender_id = request.session.session_key

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

        # logger.info(f"Rasa response status code: {rasa_response}")

        bot_message = rasa_response.json()
        # logger.info(f"bot_message-new---{bot_message}")

        if not bot_message or not isinstance(bot_message, list):
            return JsonResponse({
                "status": "error",
                "message": "No response from assistant"
            }, status=502)

        all_messages = []

        def build_message(sender_id, message_type, **kwargs):
            return {
                "sender": "bot",
                "sender_id": sender_id,
                "message_type": message_type,
                "title": kwargs.get("title", ""),
                "sections": kwargs.get("sections", []),
                "text": kwargs.get("text", ""),
                "footer": kwargs.get("footer", ""),
                "is_btn": kwargs.get("is_btn", False),
                "buttons": kwargs.get("buttons", [])
            }
        
        for msg in bot_message:
            if msg.get("custom"):
                custom_data = msg["custom"]
                all_messages.append(build_message(
                    sender_id,
                    "custom",
                    title=custom_data.get("title", ""),
                    sections=custom_data.get("sections", []),
                    # text=msg.get("text", "Emergency Instructions"),
                    footer=custom_data.get("footer", ""),
                    is_btn=bool(custom_data.get("buttons")),
                    buttons=custom_data.get("buttons", [])
                ))
            elif msg.get("buttons"):
                all_messages.append(build_message(
                    sender_id,
                    "buttons",
                    text=msg.get("text", ""),
                    is_btn=True,
                    buttons=msg.get("buttons", [])
                ))
            else:
                all_messages.append(build_message(
                    sender_id,
                    "text",
                    text=msg.get("text", "")
                ))

        return JsonResponse({"status": "success", "response": all_messages})
    except Exception as e:
        print(e)
        return JsonResponse({"status":"error","message":str(e)})