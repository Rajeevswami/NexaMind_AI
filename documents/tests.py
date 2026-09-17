from django.contrib.auth.models import User
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase
from django.urls import reverse
from .models import Document

class DocumentTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user("owner", password="StrongPass123!")
        self.other = User.objects.create_user("other", password="StrongPass123!")

    def test_documents_are_scoped_to_authenticated_owner(self):
        Document.objects.create(owner=self.other, title="private.txt", file="documents/private.txt", mime_type="text/plain", size_bytes=1)
        self.client.force_login(self.user)
        response = self.client.get(reverse("documents:index"))
        self.assertNotContains(response, "private.txt")

    def test_allowed_file_upload_creates_document(self):
        self.client.force_login(self.user)
        file = SimpleUploadedFile("notes.txt", b"hello", content_type="text/plain")
        response = self.client.post(reverse("documents:upload"), {"file": file})
        self.assertRedirects(response, reverse("documents:index"))
        self.assertTrue(Document.objects.filter(owner=self.user, title="notes.txt").exists())

