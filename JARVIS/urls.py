from django.urls import path
from .views import chat_view
from .views import home
from .views import handle_pdf_upload

urlpatterns = [
    path('', home, name='home'),
    path('chat/', chat_view, name='chat'),
    path('upload/', handle_pdf_upload, name='upload_pdf'),
]
