from django.urls import path
from core.api.views import *

urlpatterns = [
  path('category/list/', CategoryListAPIView.as_view(), name='category_list'),
]
