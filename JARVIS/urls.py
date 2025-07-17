from django.urls import path
from JARVIS import views
from .views import upload_pdf
from .views import (
    chat_view,
    home,
    upload_pdf, 
    DocumentUploadView,
    GenerateEmbeddingView,
    ChatSessionCreateView,
    ChatHistoryView,
)
from .views import contact_admin
urlpatterns = [
    path('', home, name='home'),
    path('chat/', chat_view, name='chat'),
    path('upload/', views.upload_pdf, name='upload'),
    path('register/', views.register_view, name='register'),
    path('contact/', contact_admin, name='contact'),

    # REST API endpoints
    path('api/documents/upload/', DocumentUploadView.as_view(), name='document-upload'),
    path('api/embeddings/generate/', GenerateEmbeddingView.as_view(), name='generate-embedding'),
    path('api/chat_sessions/create/', ChatSessionCreateView.as_view(), name='chat-session-create'),
    path('api/chat_sessions/<int:session_id>/history/', ChatHistoryView.as_view(), name='chat-history'),
]
