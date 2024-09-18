# urls.py

from django.urls import path
from .views import add_player, create_tournament, match_summary, scoring_home
from .views import view_stats, batting_stats, bowling_stats, batting_stat_detail, bowling_stat_detail

urlpatterns = [
    path('', scoring_home, name='scoring_home'),  # Home page
    path('add_player/', add_player, name='add_player'),  # Add player page
    path('create_tournament/', create_tournament, name='create_tournament'),  # Create tournament page
    path('match_summary/<uuid:tournament_id>/<int:match_number>/<int:num_players>/', match_summary, name='match_summary'),  # Match summary page
    path('view_stats/', view_stats, name='view_stats'),  # View stats page
    path('batting_stats/', batting_stats, name='batting_stats'),
    path('batting_stats/<str:stat_type>/', batting_stat_detail, name='batting_stat_detail'),
    path('bowling_stats/', bowling_stats, name='bowling_stats'),
    path('bowling_stats/<str:stat_type>/', bowling_stat_detail, name='bowling_stat_detail'),
]
