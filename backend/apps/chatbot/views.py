from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status

from .serializers import ChatRequestSerializer
from .models import ChatHistory
from services.ai_services.insight_generator import ask_financial_ai


class FinancialChatAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = ChatRequestSerializer(data=request.data)
        if serializer.is_valid():
            question = serializer.validated_data["question"]
            ai_result = ask_financial_ai(user=request.user, question=question)

            ChatHistory.objects.create(
                user=request.user,
                question=question,
                response=ai_result["response"],
            )

            return Response(
                {
                    "success": True,
                    "question": question,
                    "response": ai_result["response"],
                    "context": ai_result["context"],
                },
                status=status.HTTP_200_OK,
            )

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
