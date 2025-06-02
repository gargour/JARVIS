from rest_framework import generics, status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser, FormParser
from django.shortcuts import get_object_or_404

from .models import Document, Embedding, ChatSession
from .serializers import DocumentSerializer, EmbeddingSerializer, ChatSessionSerializer

# Upload document (fichier PDF)
class DocumentUploadView(generics.CreateAPIView):
    queryset = Document.objects.all()
    serializer_class = DocumentSerializer
    parser_classes = [MultiPartParser, FormParser]

# Génération d'Embedding - ici on simule la génération
class GenerateEmbeddingView(APIView):
    def post(self, request, *args, **kwargs):
        document_id = request.data.get('document')
        vector = request.data.get('vector')  # attend un JSON array de floats
        
        if not document_id or not vector:
            return Response({"error": "document et vector sont requis"}, status=status.HTTP_400_BAD_REQUEST)
        
        document = get_object_or_404(Document, pk=document_id)
        
        # Vérification simple sur la taille du vecteur
        if not isinstance(vector, list) or len(vector) != 768:
            return Response({"error": "vector doit être une liste de 768 floats"}, status=status.HTTP_400_BAD_REQUEST)
        
        embedding = Embedding.objects.create(document=document, vector=vector)
        serializer = EmbeddingSerializer(embedding)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

# Création d'une session de chat
class ChatSessionCreateView(generics.CreateAPIView):
    queryset = ChatSession.objects.all()
    serializer_class = ChatSessionSerializer

# Consultation de l’historique d’une session de chat
class ChatHistoryView(APIView):
    def get(self, request, session_id):
        session = get_object_or_404(ChatSession, pk=session_id)
        serializer = ChatSessionSerializer(session)
        return Response(serializer.data)
