from django.urls import path
from .views import (
    chat_view,
    home,
    handle_pdf_upload,
    DocumentUploadView,
    GenerateEmbeddingView,
    ChatSessionCreateView,
    ChatHistoryView,
)

urlpatterns = [
    path('', home, name='home'),
    path('chat/', chat_view, name='chat'),
    path('upload/', handle_pdf_upload, name='upload_pdf'),

    # REST API endpoints
    path('api/documents/upload/', DocumentUploadView.as_view(), name='document-upload'),
    path('api/embeddings/generate/', GenerateEmbeddingView.as_view(), name='generate-embedding'),
    path('api/chat_sessions/create/', ChatSessionCreateView.as_view(), name='chat-session-create'),
    path('api/chat_sessions/<int:session_id>/history/', ChatHistoryView.as_view(), name='chat-history'),
]
