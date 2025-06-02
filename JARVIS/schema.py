import graphene
from graphene_django import DjangoObjectType
from .models import Document, Embedding, ChatSession, ChatMessage

# Types

class DocumentType(DjangoObjectType):
    class Meta:
        model = Document
        fields = ('id', 'title', 'upload_date', 'file', 'text_content')

class EmbeddingType(DjangoObjectType):
    class Meta:
        model = Embedding
        fields = ('id', 'document', 'vector', 'created_at')

class ChatMessageType(DjangoObjectType):
    class Meta:
        model = ChatMessage
        fields = ('id', 'session', 'sender', 'message', 'created_at')

class ChatSessionType(DjangoObjectType):
    class Meta:
        model = ChatSession
        fields = ('id', 'user', 'session_name', 'started_at', 'ended_at', 'messages')

# Queries

class Query(graphene.ObjectType):
    all_documents = graphene.List(DocumentType)
    document_by_id = graphene.Field(DocumentType, id=graphene.Int(required=True))
    
    all_chat_sessions = graphene.List(ChatSessionType)
    chat_session_by_id = graphene.Field(ChatSessionType, id=graphene.Int(required=True))

    def resolve_all_documents(root, info):
        return Document.objects.all()

    def resolve_document_by_id(root, info, id):
        return Document.objects.get(pk=id)

    def resolve_all_chat_sessions(root, info):
        return ChatSession.objects.all()

    def resolve_chat_session_by_id(root, info, id):
        return ChatSession.objects.get(pk=id)

# Mutations (exemple pour créer Document)

class CreateDocument(graphene.Mutation):
    document = graphene.Field(DocumentType)

    class Arguments:
        title = graphene.String(required=True)
        file = graphene.String(required=True)  # Ici tu peux adapter pour l’upload fichier réel (via base64, etc.)
        text_content = graphene.String()

    def mutate(self, info, title, file, text_content=None):
        document = Document(title=title, file=file, text_content=text_content)
        document.save()
        return CreateDocument(document=document)

class Mutation(graphene.ObjectType):
    create_document = CreateDocument.Field()

schema = graphene.Schema(query=Query, mutation=Mutation)
