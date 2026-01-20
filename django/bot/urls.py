from django.urls import path
from .views import index, handle_user_message

urlpatterns = [
    path('', index, name='bot-index'),
    path('get_response/', handle_user_message, name='get-response'),
]
