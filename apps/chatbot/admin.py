from django.contrib import admin

from .models import ChatMessage, Document


@admin.register(Document)
class DocumentAdmin(admin.ModelAdmin):
    list_display = ("id", "uploaded_at")
    search_fields = ("id",)


@admin.register(ChatMessage)
class ChatMessageAdmin(admin.ModelAdmin):
    list_display = ("id", "document", "created_at")
    search_fields = ("question", "answer")
    list_filter = ("created_at",)

