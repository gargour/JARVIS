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
from django.shortcuts import render

def upload_pdf(request):
    # Affiche un formulaire ou gère l'upload selon tes besoins
    return render(request, 'chatbot/upload_pdf.html')


from django.core.mail import send_mail
from django.conf import settings
from django.shortcuts import render

def contact_admin(request):
    success = None
    if request.method == "POST":
        name = request.POST.get("name")
        email = request.POST.get("email")
        message = request.POST.get("message")
        full_message = f"Message de {name} <{email}> :\n\n{message}"

        send_mail(
            subject="Nouveau message via le formulaire de contact",
            message=full_message,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=["amr.gara@sesame.com.tn"],
        )
        success = "Votre message a bien été envoyé !"
    return render(request, "chatbot/contact.html", {"success": success})
from .forms import RegisterForm


def register_view(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("login")  # Ou la page d'accueil selon tes besoins
    else:
        form = RegisterForm()
    return render(request, 'chatbot/register.html', {'form': form})







from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            login(request, form.get_user())
            return render(request, 'chatbot/home.html', {'form': form})  # ou une autre vue
    else:
        form = AuthenticationForm()
    return render(request, 'chatbot/login.html', {'form': form})

def cree_view(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return render(request, 'chatbot/home.html', {'form': form})
    else:
        form = UserCreationForm()
    return render(request, 'chatbot/register.html', {'form': form})
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