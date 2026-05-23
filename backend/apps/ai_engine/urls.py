from django.urls import path

from .views import (
    AISummaryAPIView,
    AIRecommendationsAPIView,
    AIRiskAnalysisAPIView,
    AIForecastAPIView,
)

urlpatterns = [
    path("ai/summary/", AISummaryAPIView.as_view(), name="ai-summary"),
    path("ai/recommendations/", AIRecommendationsAPIView.as_view(), name="ai-recommendations"),
    path("ai/risk-analysis/", AIRiskAnalysisAPIView.as_view(), name="ai-risk-analysis"),
    path("ai/forecast/", AIForecastAPIView.as_view(), name="ai-forecast"),
]
