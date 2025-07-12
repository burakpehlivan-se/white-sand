# urls.py
from django.urls import path
from . import views
from .views import ajax_get_recommendation

urlpatterns = [
    path('', views.home, name='index'),
    path('preferences/', views.preference_view, name='preferences'),
    path('about/', views.about_view, name='about'),
    path('dashboard/', views.dashboard_view, name='dashboard'),
    path('recommendation-quiz/', views.recommendation_quiz_view, name='recommendation_quiz'),
    path('past-recommendations/', views.past_recommendations, name='past_recommendations'),
    path('search/', views.search_destinations, name='search_destinations'),
    path('ajax/get-recommendation/', ajax_get_recommendation, name='ajax_get_recommendation')
]