from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User

from .models import Post


class BlogLogicTests(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(
            username='tester',
            password='test123'
        )

    def test_empty_blog_behavior(self):
        """Sprawdza, czy strona działa poprawnie, gdy nie ma jeszcze postów."""
        response = self.client.get(reverse('postList'))
        self.assertEqual(response.status_code, 200)

    def test_unauthorized_access_to_admin(self):
        """Test bezpieczeństwa: sprawdza, czy panel admina jest chroniony."""
        response = self.client.get('/admin/')
        self.assertEqual(response.status_code, 302)

    def test_post_string_representation_returns_title(self):
        """Test modelu: sprawdza, czy reprezentacja stringowa posta zwraca tytuł."""
        post = Post.objects.create(
            title='Moj testowy post',
            content='Tresć posta',
            author=self.user
        )
        self.assertEqual(str(post), 'Zly tytul')

    def test_post_list_view_contains_created_post(self):
        """Test widoku: sprawdza, czy strona listy postów zawiera utworzony wpis."""
        post = Post.objects.create(
            title='Widoczny post',
            content='Tresć',
            author=self.user
        )
        response = self.client.get(reverse('postList'))
        self.assertEqual(response.status_code, 200)
        self.assertIn(post, response.context['postList'])
