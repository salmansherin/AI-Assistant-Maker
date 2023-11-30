from django.urls import path
from .views import assistant

urlpatterns = [
    path('', assistant.DashboardView.as_view(), name='dashboard'),
    path('create', assistant.CreateView.as_view(), name='create_assistant'),
    path('chat', assistant.ChatAjaxView.as_view(), name='chat'),
    path('edit/<str:assistant_id>/', assistant.EditView.as_view(), name='edit_assistant'),
    path('test/<str:assistant_id>/', assistant.ChatView.as_view(), name='test_assistant'),
    path('files/<str:assistant_id>', assistant.AssistantFilesView.as_view(), name='assistant_files'),
]
