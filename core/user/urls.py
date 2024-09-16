from django.urls import path
from core.user.views import *

urlpatterns = [
    # user
    path('user/', UserListView.as_view(), name='user_list'),
    path('user/add/', UserCreateView.as_view(), name='user_create'),
    path('user/update/<int:pk>/', UserUpdateView.as_view(), name='user_update'),
    path('user/delete/<int:pk>/', UserDeleteView.as_view(), name='user_delete'),
    path('user/choose/profile/<int:pk>/', UserChooseGroup.as_view(), name='user_choose_profile'),
    path('user/update/profile/', UserUpdateProfileView.as_view(), name='user_update_profile'),
    path('user/change/password/', UserChangePasswordView.as_view(), name='user_change_password'),
]
