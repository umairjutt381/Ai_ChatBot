from django.urls import path

from .views import ChatView, UploadDocumentView, chat_page, entrypoint

app_name = "chatbot"

urlpatterns = [
    path("", entrypoint, name="home"),
    path("app/", chat_page, name="app"),
    path("api/upload/", UploadDocumentView.as_view(), name="upload"),
    path("api/chat/", ChatView.as_view(), name="chat"),
]

