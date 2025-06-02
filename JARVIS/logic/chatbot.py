import fitz
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.docstore.document import Document
from langchain_community.vectorstores import FAISS
from langchain_ollama import OllamaLLM  # Changement ici : nouvelle importation
import os
from langchain_huggingface import HuggingFaceEmbeddings

embeddings = HuggingFaceEmbeddings(model_name="all-mpnet-base-v2")
PDF_PATH = r"C:\Users\amrga\OneDrive\Desktop\New folder\CV Amr GARA.pdf"
CHUNK_SIZE = 1000
CHUNK_OVERLAP = 200
LLM_MODEL = "mistral"

filename, text, retriever = None, None, None

def setup_bot():
    global filename, text, retriever
    if not retriever:
        if not os.path.exists(PDF_PATH):
            raise FileNotFoundError(f"❌ Fichier non trouvé : {PDF_PATH}")
        doc = fitz.open(PDF_PATH)
        text = "".join(page.get_text("text") for page in doc)
        filename = os.path.basename(PDF_PATH)
        splitter = RecursiveCharacterTextSplitter(
            chunk_size=CHUNK_SIZE,
            chunk_overlap=CHUNK_OVERLAP,
            separators=["\n\n", "\n", " ", ""]
        )
        chunks = splitter.split_text(text)
        docs = [Document(page_content=chunk) for chunk in chunks]
        embeddings = HuggingFaceEmbeddings()
        faiss_db = FAISS.from_documents(docs, embeddings)
        retriever = faiss_db.as_retriever()

def get_bot_response(query):
    setup_bot()
    llm = OllamaLLM(model=LLM_MODEL)  # Utiliser la nouvelle classe

    # Utiliser invoke() au lieu de get_relevant_documents()
    docs = retriever.invoke(query)[:3]  # Vérifie la doc selon ton retriever

    context = "\n\n".join(d.page_content for d in docs)

    prompt = f"""
Voici des extraits du document « {filename} » :
---
{context}
---

Votre tâche :
1. Répondez **uniquement** en **copiant exactement** une des phrases ou paragraphes ci-dessus.
2. Ne paraphrasez pas, ne résumez pas.
3. Si aucune information ne répond à la question, répondez exactement :
« Je n'ai pas trouvé la réponse dans le document. »

Question : {query}

Réponse :
""".strip()

    # Utiliser invoke() pour appeler le LLM
    response = llm.invoke(prompt)
    return response
