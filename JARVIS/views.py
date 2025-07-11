from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from rest_framework import generics, status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser, FormParser

from .logic.chatbot import get_bot_response
from .models import Document, Embedding, ChatSession
from .serializers import DocumentSerializer, EmbeddingSerializer, ChatSessionSerializer

# Vues classiques

def chat_view(request):
    response = ""
    if request.method == "POST":
        question = request.POST.get("question", "").strip()
        if question:
            response = get_bot_response(question)
    return render(request, "chatbot/chat.html", {"response": response})

def home(request):
    return render(request, "chatbot/home.html")
def handle_pdf_upload(request):
    return HttpResponse("PDF upload handler.")

# Vues API REST

class DocumentUploadView(generics.CreateAPIView):
    queryset = Document.objects.all()
    serializer_class = DocumentSerializer
    parser_classes = [MultiPartParser, FormParser]

class GenerateEmbeddingView(APIView):
    def post(self, request, *args, **kwargs):
        document_id = request.data.get('document')
        vector = request.data.get('vector')  # Doit être une liste de floats
        
        if not document_id or not vector:
            return Response({"error": "document et vector sont requis"}, status=status.HTTP_400_BAD_REQUEST)
        
        document = get_object_or_404(Document, pk=document_id)
        
        if not isinstance(vector, list) or len(vector) != 768:
            return Response({"error": "vector doit être une liste de 768 floats"}, status=status.HTTP_400_BAD_REQUEST)
        
        embedding = Embedding.objects.create(document=document, vector=vector)
        serializer = EmbeddingSerializer(embedding)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

class ChatSessionCreateView(generics.CreateAPIView):
    queryset = ChatSession.objects.all()
    serializer_class = ChatSessionSerializer
class ChatHistoryView(APIView):
    def get(self, request, session_id):
        session = get_object_or_404(ChatSession, pk=session_id)
        serializer = ChatSessionSerializer(session)
        return Response(serializer.data, status=status.HTTP_200_OK)