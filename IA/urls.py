from django.contrib import admin
from django.urls import path, include
from JARVIS import views  # ✅ Import manquant

urlpatterns = [
    path('admin/', admin.site.urls),

    # Authentification
    path('register/', views.register_view, name='register'),
    path('login/', views.login_view, name='login'),

    # Accueil = page de login
    path('', views.login_view, name='home'),

    # Chat
    path('chat/', views.chat_view, name='chat'),

    path('upload/', views.upload_pdf, name='upload'),
    # Inclure d'autres URLs (si besoin)
    path('jarvis/', include('JARVIS.urls')),
]