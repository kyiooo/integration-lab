from django.urls import path
from .views import PostListView, PostDetailView

urlpatterns = [
    # Strona główna bloga
    path('', PostListView.as_view(), name='postList'),

    # Szczegóły posta
    path('post/<int:pk>/', PostDetailView.as_view(), name='postDetail'),
]
