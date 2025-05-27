from django.shortcuts import render
from .logic.chatbot import get_bot_response

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
from django.http import HttpResponse

def handle_pdf_upload(request):
    return HttpResponse("PDF upload handler.")

