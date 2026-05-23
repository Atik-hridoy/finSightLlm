from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status

from .serializers import AIRequestSerializer
from .services import (
    generate_summary,
    generate_recommendations,
    generate_risk_analysis,
    generate_forecast,
)


class AISummaryAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = AIRequestSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        result = generate_summary(request.user)
        return Response(result, status=status.HTTP_200_OK)


class AIRecommendationsAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = AIRequestSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        result = generate_recommendations(request.user)
        return Response(result, status=status.HTTP_200_OK)


class AIRiskAnalysisAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = AIRequestSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        result = generate_risk_analysis(request.user)
        return Response(result, status=status.HTTP_200_OK)


class AIForecastAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = AIRequestSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        result = generate_forecast(request.user)
        return Response(result, status=status.HTTP_200_OK)
