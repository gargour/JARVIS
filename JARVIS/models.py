import os
from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError

def validate_pdf_file(file):
    valid_extensions = ['.pdf']
    ext = os.path.splitext(file.name)[1].lower()
    if ext not in valid_extensions:
        raise ValidationError('Seuls les fichiers PDF sont autorisés.')

def validate_embedding_dimension(value):
    expected_dim = 768
    if not isinstance(value, list):
        raise ValidationError('L\'embedding doit être une liste.')
    if len(value) != expected_dim:
        raise ValidationError(f'L\'embedding doit avoir une dimension de {expected_dim}.')
    if not all(isinstance(x, (float, int)) for x in value):
        raise ValidationError('Tous les éléments de l\'embedding doivent être des nombres.')

class Document(models.Model):
    title = models.CharField(max_length=255)
    upload_date = models.DateTimeField(auto_now_add=True)
    file = models.FileField(upload_to='documents/', validators=[validate_pdf_file])
    text_content = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.title

class Embedding(models.Model):
    document = models.ForeignKey(Document, on_delete=models.CASCADE, related_name='embeddings')
    vector = models.JSONField(validators=[validate_embedding_dimension])
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Embedding for {self.document.title} ({self.id})"

class ChatSession(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    session_name = models.CharField(max_length=255, blank=True)
    started_at = models.DateTimeField(auto_now_add=True)
    ended_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"ChatSession {self.id} - {self.session_name or 'No name'}"

class ChatMessage(models.Model):
    session = models.ForeignKey(ChatSession, on_delete=models.CASCADE, related_name='messages')
    sender = models.CharField(max_length=10, choices=[('user', 'User'), ('bot', 'Bot')])
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['created_at']

    def __str__(self):
        return f"{self.sender} @ {self.created_at.strftime('%Y-%m-%d %H:%M:%S')}"
