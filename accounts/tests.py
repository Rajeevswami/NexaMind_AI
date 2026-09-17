from django.test import TestCase
from django.urls import reverse

class RegistrationTests(TestCase):
    def test_user_can_register_and_reach_dashboard(self):
        response = self.client.post(reverse("register"), {
            "username": "nexa", "email": "nexa@example.com",
            "password1": "StrongPass123!", "password2": "StrongPass123!",
        })
        self.assertRedirects(response, reverse("dashboard:home"))
        self.assertTrue(response.wsgi_request.user.is_authenticated)
        self.assertTrue(response.wsgi_request.user.profile)
