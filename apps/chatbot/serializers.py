from rest_framework import serializers


class UploadDocumentSerializer(serializers.Serializer):
    file = serializers.FileField()


class ChatRequestSerializer(serializers.Serializer):
    question = serializers.CharField(max_length=2000)

