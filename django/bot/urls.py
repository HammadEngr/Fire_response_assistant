from django.urls import path
from .views import chat, index

urlpatterns = [
    path('', index, name='bot-index'),
    path('chat/', chat, name='chat-page'),
]
