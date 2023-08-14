from django.urls import path

from posts.views import PostListView, PostCountView, PostRetrieveView, PostCreateView, PostReportView

app_name = 'posts'

urlpatterns = [
    path('', PostListView.as_view(), name='post-list'),
    path('count/', PostCountView.as_view(), name='post-count'),
    path('<int:pk>/', PostRetrieveView.as_view(), name='post-detail'),
    path('create/', PostCreateView.as_view(), name='post-create'),
    path('report/<int:pk>', PostReportView.as_view(), name='post-report'),
]