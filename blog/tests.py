from django.test import TestCase
from django.urls import reverse
from .models import Post
from django.contrib.auth.models import User

class BlogLogicTests(TestCase):
    
    def test_empty_blog_behavior(self):
        """Sprawdza, czy strona działa poprawnie, gdy nie ma jeszcze postów."""
        response = self.client.get(reverse('postList'))
        self.assertEqual(response.status_code, 200)

    def test_unauthorized_access_to_admin(self):
        """Test bezpieczeństwa: sprawdza, czy panel admina jest chroniony."""
        response = self.client.get('/admin/')
        self.assertEqual(response.status_code, 302)