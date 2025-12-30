from django.urls import path
from .views import index, handle_user_message

urlpatterns = [
    path('', index, name='bot-index'),
    # path('chat/', chat, name='chat-page'),

    path('get_response/', handle_user_message, name='get-response'),
]
