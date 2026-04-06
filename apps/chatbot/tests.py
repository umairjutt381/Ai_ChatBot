from django.core.files.uploadedfile import SimpleUploadedFile
from django.contrib.auth.models import User
from django.test import TestCase
from rest_framework.test import APIClient


class ChatbotApiTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.username = "alice"
        self.password = "StrongPass123!"
        self.user = User.objects.create_user(username=self.username, password=self.password)

    def test_root_redirects_anonymous_to_register(self):
        response = self.client.get("/")
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, "/register/")

    def test_login_then_root_redirects_to_app(self):
        self.client.login(username=self.username, password=self.password)
        response = self.client.get("/")
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, "/app/")

    def test_api_requires_authentication(self):
        response = self.client.post("/api/chat/", {"question": "What is this?"}, format="json")
        self.assertIn(response.status_code, (401, 403))

    def test_authenticated_chat_requires_document_upload(self):
        self.client.login(username=self.username, password=self.password)
        response = self.client.post("/api/chat/", {"question": "What is this?"}, format="json")
        self.assertEqual(response.status_code, 400)
        self.assertIn("error", response.json())

    def test_upload_then_chat(self):
        self.client.login(username=self.username, password=self.password)
        content = b"Django is a Python web framework. It helps build secure applications."
        upload = SimpleUploadedFile("doc.txt", content, content_type="text/plain")

        upload_response = self.client.post("/api/upload/", {"file": upload}, format="multipart")
        self.assertEqual(upload_response.status_code, 201)

        chat_response = self.client.post("/api/chat/", {"question": "What is Django?"}, format="json")
        self.assertEqual(chat_response.status_code, 200)
        self.assertIn("answer", chat_response.json())
        self.assertTrue(chat_response.json()["answer"])

