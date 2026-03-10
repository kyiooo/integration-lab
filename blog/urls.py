from django.urls import path
from .views import PostListView, PostDetailView

urlpatterns = [
    path('', PostListView.as_view(), name='postList'),  # Strona główna bloga
    path('post/<int:pk>/', PostDetailView.as_view(), name='postDetail'), # Szczegóły posta
]