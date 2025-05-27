# IA/urls.py

from django.contrib import admin
from django.urls import path, include
from JARVIS import views  # ✅ Import manquant

urlpatterns = [
    path('admin/', admin.site.urls),
    path('chat/', views.chat_view, name='chat'),
    path('', views.home, name='home'),  # si tu as une page d'accueil
     path('', include('JARVIS.urls')),
]