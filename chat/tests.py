from unittest.mock import patch
from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse
from .models import ChatSession

class ChatApiTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user("chatowner", password="StrongPass123!")
        self.other = User.objects.create_user("otheruser", password="StrongPass123!")
        self.client.force_login(self.user)

    def test_session_list_is_private(self):
        ChatSession.objects.create(owner=self.other, title="Private")
        self.assertEqual(self.client.get(reverse("chat:session_list")).json()["sessions"], [])

    @patch("chat.views.requests.post")
    def test_successful_message_saves_both_turns(self, post):
        post.return_value.raise_for_status.return_value = None
        post.return_value.json.return_value = {"answer": "A queue is FIFO."}
        session = ChatSession.objects.create(owner=self.user)
        response = self.client.post(reverse("chat:send_message", args=[session.id]), data='{"message":"What is a queue?"}', content_type="application/json")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(list(session.messages.values_list("role", flat=True)), ["user", "assistant"])
