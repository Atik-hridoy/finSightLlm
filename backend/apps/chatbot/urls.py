from django.urls import path
from .views import FinancialChatAPIView

urlpatterns = [
    path("chat/", FinancialChatAPIView.as_view(), name="financial-chat"),
]
