# scoring/forms.py

from django import forms
from django.forms import modelformset_factory
from .models import Player, Match

class PlayerForm(forms.ModelForm):
    class Meta:
        model = Player
        fields = ['name', 'dob', 'image']

class MatchForm(forms.ModelForm):
    class Meta:
        model = Match
        fields = [
            'player', 'runs_scored', 'balls_faced', 'is_out',
            'balls_bowled', 'runs_conceded', 'wickets_taken',
            'is_common_player', 'match_won'
        ]

MatchFormSet = modelformset_factory(Match, form=MatchForm, extra=0)
