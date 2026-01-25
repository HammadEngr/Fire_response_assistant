from django.urls import path
from .views import index, handle_user_message, get_save_location

urlpatterns = [
    path('', index, name='bot-index'),
    path("send_location/", get_save_location, name="send-location"),
    path('get_response/', handle_user_message, name='get-response'),
]
