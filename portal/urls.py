from django.urls import path
from .views import *

urlpatterns = [
    path('', portal, name='portal'),
    # path('register/', register, name='register'),
    path('login/', log_in, name='log_in'),  
    path('logout/', logoutUser, name='logout'), 
    path('admin/', admin, name='admin'), 
    path('admin/conversations/', admin_conversations, name='admin_conversations'),
    path('admin/conversations/<int:user_id>/', admin_chat, name='admin_chat'),  # Ensure this is for viewing chat
    path('get_messages/<int:user_id>/', get_messages, name='get_messages'),  # URL for fetching messages
    path('admin/conversations/delete/', delete_conversation, name='delete_conversation'),
    path('delete_chats/', delete_chats, name='delete_chats'),  # URL for deleting chats
    path('admin/check_new_users/', check_new_users, name='check_new_users'),
    # path('change_password/', change_password, name='change_password'),  # URL for password change
    path('change_password/', change_password, name='change_password'),
    path('admissions/download/', download_admissions_pdf, name='download_admissions_pdf'),
]
