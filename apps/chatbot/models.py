from django.db import models


class Document(models.Model):
    file = models.FileField(upload_to="docs/")
    extracted_text = models.TextField(blank=True)
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Document {self.pk}"


class ChatMessage(models.Model):
    document = models.ForeignKey(Document, on_delete=models.CASCADE, related_name="messages")
    question = models.TextField()
    answer = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"ChatMessage {self.pk} for Document {self.document_id}"
