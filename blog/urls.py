from django.urls import path
from . import views
from .views import PostListViews, PostDetailViews, PostCreateView, PostUpdateView

urlpatterns = [path('', PostListViews.as_view(), name='blog-home'),
               # .as_view() to convert class into actual view.
               path('post/<int:pk>/', PostDetailViews.as_view(), name='post-detail'),
               path('post/new/', PostCreateView.as_view(), name='post-create'),
               path('post/<int:pk>/update/', PostUpdateView.as_view(), name='post-update'),
               path('about/', views.about, name='blog-about'), ]
