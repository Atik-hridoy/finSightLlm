from django.contrib import admin
from .models import ChatHistory


@admin.register(ChatHistory)
class ChatHistoryAdmin(admin.ModelAdmin):
    list_display = ("user", "created_at", "question")
    search_fields = ("user__username", "question", "response")
    list_filter = ("created_at",)
