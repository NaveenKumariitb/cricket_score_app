

from django.shortcuts import render, redirect, get_object_or_404
from django.forms import formset_factory
from .forms import PlayerForm, MatchForm
from .models import Player, Tournament, Match

from django.db.models import Sum, Avg, F, ExpressionWrapper, FloatField, Max, Value,CharField,IntegerField,When,Case
from .models import Player, Match
from django.db.models.functions import Concat, Cast, Coalesce

from django.forms import formset_factory



def match_summary(request, tournament_id, match_number, num_players):
    tournament = get_object_or_404(Tournament, tournament_id=tournament_id)
    num_rows = num_players + 1 if num_players % 2 != 0 else num_players
    
    # Create a formset factory with the desired number of forms
    MatchFormSet = formset_factory(MatchForm, extra=num_rows)
    
    if request.method == 'POST':
        formset = MatchFormSet(request.POST, request.FILES)
        if formset.is_valid():
            for form in formset:
                match = form.save(commit=False)
                match.tournament = tournament
                match.save()
            
            if 'end_series' in request.POST:
                return redirect('tournament_summary', tournament_id=tournament_id)
            else:
                next_match = match_number + 1
                if next_match > 3:
                    return redirect('tournament_summary', tournament_id=tournament_id)
                else:
                    return redirect('match_summary', tournament_id=tournament_id, match_number=next_match, num_players=num_players)
    else:
        formset = MatchFormSet()  # Initialize with the default number of empty forms

    return render(request, 'scoring/match_summary.html', {
        'formset': formset,
        'tournament': tournament,
        'match_number': match_number,
    })


def scoring_home(request):
    return render(request, 'scoring/home.html')


def add_player(request):
    if request.method == 'POST':
        form = PlayerForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('add_player')
    else:
        form = PlayerForm()
    return render(request, 'scoring/add_player.html', {'form': form})

def create_tournament(request):
    if request.method == 'POST':
        num_players = int(request.POST['num_players'])
        tournament = Tournament.objects.create()
        return redirect('match_summary', tournament_id=tournament.tournament_id, match_number=1, num_players=num_players)
    return render(request, 'scoring/create_tournament.html')



def view_stats(request):
    return render(request, 'scoring/view_stats.html')


def batting_stats(request):
    return render(request, 'scoring/batting_stats.html')

def bowling_stats(request):
    return render(request, 'scoring/bowling_stats.html')


def batting_stat_detail(request, stat_type):
    if stat_type == 'total_runs':
        players = Player.objects.annotate(
            total_runs=Sum('match__runs_scored')
        ).order_by('-total_runs')[:5]
        stat_label = 'Total Runs'
    elif stat_type == 'batting_avg':
        players = Player.objects.annotate(
            total_runs=Sum('match__runs_scored'),
            total_out=Sum(Case(When(match__is_out=True, then=1), default=0, output_field=IntegerField())),
        ).annotate(
            batting_avg=ExpressionWrapper(
                F('total_runs') / (F('total_out') or 1),
                output_field=FloatField()
            )
        ).order_by('-batting_avg')[:5]
        stat_label = 'Batting Average'
    elif stat_type == 'strike_rate':
        players = Player.objects.annotate(
            total_runs=Sum('match__runs_scored'),
            total_balls=Sum('match__balls_faced'),
        ).annotate(
            strike_rate=ExpressionWrapper(
                (F('total_runs') * 100) / (F('total_balls') or 1),
                output_field=FloatField()
            )
        ).order_by('-strike_rate')[:5]
        stat_label = 'Strike Rate'
    elif stat_type == 'highest_score':
        players = Player.objects.annotate(
            highest_score=Max('match__runs_scored')
        ).order_by('-highest_score')[:5]
        stat_label = 'Highest Score'
    return render(request, 'stats_detail.html', {'players': players, 'stat_label': stat_label, 'stat_title': 'Batting Stats', 'stat_type': stat_type})

def bowling_stat_detail(request, stat_type):
    if stat_type == 'total_wickets':
        players = Player.objects.annotate(
            total_wickets=Sum('match__wickets_taken')
        ).order_by('-total_wickets')[:5]
        stat_label = 'Total Wickets'
    elif stat_type == 'economy_rate':
        players = Player.objects.annotate(
            total_runs=Sum('match__runs_conceded'),
            total_balls=Sum('match__balls_bowled'),
        ).annotate(
            economy_rate=ExpressionWrapper(
                (F('total_runs') * 6) / (F('total_balls') or 1),
                output_field=FloatField()
            )
        ).order_by('economy_rate')[:5]
        stat_label = 'Economy Rate'
    elif stat_type == 'bowling_avg':
        players = Player.objects.annotate(
            total_runs=Sum('match__runs_conceded'),
            total_wickets=Sum('match__wickets_taken')
        ).annotate(
            bowling_avg=ExpressionWrapper(
                F('total_runs') / (F('total_wickets') or 1),
                output_field=FloatField()
            )
        ).order_by('bowling_avg')[:5]
        stat_label = 'Bowling Average'
    elif stat_type == 'best_bowling_figure':
        players = Player.objects.annotate(
            best_bowling_figure=Concat(
                Sum('match__wickets_taken'),
                Value('-'),
                Sum('match__runs_conceded'),
                Value('('),
                ExpressionWrapper(Sum('match__balls_bowled') / 6, output_field=FloatField()),
                Value(')')
            )
        ).order_by('-best_bowling_figure')[:5]
        stat_label = 'Best Bowling Figure'
    return render(request, 'stats_detail.html', {'players': players, 'stat_label': stat_label, 'stat_title': 'Bowling Stats', 'stat_type': stat_type})

