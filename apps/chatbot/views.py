from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import get_object_or_404, redirect, render
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.parsers import FormParser, MultiPartParser
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import ChatMessage, Document
from .serializers import ChatRequestSerializer, UploadDocumentSerializer
from .services.chains import build_qa_chain
from .services.document_loader import load_document
from .services.embeddings import get_embeddings
from .services.vector_store import create_vector_store


def entrypoint(request):
    if request.user.is_authenticated:
        return redirect("chatbot:app")
    return redirect("register")


def register_view(request):
    if request.user.is_authenticated:
        return redirect("chatbot:app")

    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Account created. Please login.")
            return redirect("login")
    else:
        form = UserCreationForm()

    return render(request, "registration/register.html", {"form": form})


@login_required
def chat_page(request):
    return render(request, "chatbot/index.html")


class UploadDocumentView(APIView):
    permission_classes = [IsAuthenticated]
    parser_classes = [MultiPartParser, FormParser]

    def post(self, request):
        serializer = UploadDocumentSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        uploaded_file = serializer.validated_data["file"]
        document = Document.objects.create(file=uploaded_file)

        text = load_document(document.file.path)
        document.extracted_text = text
        document.save(update_fields=["extracted_text"])

        request.session["document_id"] = document.id

        return Response(
            {
                "message": "Document uploaded successfully.",
                "document_id": document.id,
                "chars_loaded": len(text),
            },
            status=status.HTTP_201_CREATED,
        )


class ChatView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = ChatRequestSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        document_id = request.session.get("document_id")
        if not document_id:
            return Response(
                {"error": "Please upload a document first."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        document = get_object_or_404(Document, pk=document_id)
        embeddings = get_embeddings()
        vector_store = create_vector_store(document.extracted_text, embeddings)
        qa_chain = build_qa_chain(vector_store)

        question = serializer.validated_data["question"]
        answer = qa_chain.run(question)

        ChatMessage.objects.create(document=document, question=question, answer=answer)

        return Response({"answer": answer}, status=status.HTTP_200_OK)
