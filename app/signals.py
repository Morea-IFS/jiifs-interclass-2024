# app/signals.py
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
from .models import Point, Match, Team_match

@receiver(post_save, sender=Point)
def point_saved(sender, instance, created, **kwargs):
    # Recupere a partida atual
    if created:
        match = Match.objects.get(status=1)
        team_matchs = Team_match.objects.filter(match=match)
        team_match_a = team_matchs[0]
        team_match_b = team_matchs[1]
        
        # Conte os pontos
        point_a = Point.objects.filter(team_match=team_match_a).count()
        point_b = Point.objects.filter(team_match=team_match_b).count()

        # Envia dados atualizados para o WebSocket
        channel_layer = get_channel_layer()
        async_to_sync(channel_layer.group_send)(
            "placar",
            {
                'type': 'send_score',
                'score': {
                    'team_a': team_match_a.team.name,
                    'team_b': team_match_b.team.name,
                    'points_a': point_a,
                    'points_b': point_b,
                },
            }
        )

@receiver(post_delete, sender=Point)
def point_removed(sender, instance, using, **kwargs):
    # Recupere a partida atual
    match = Match.objects.get(status=1)
    team_matchs = Team_match.objects.filter(match=match)
    team_match_a = team_matchs[0]
    team_match_b = team_matchs[1]
    
    # Conte os pontos
    point_a = Point.objects.filter(team_match=team_match_a).count()
    point_b = Point.objects.filter(team_match=team_match_b).count()

    # Envia dados atualizados para o WebSocket
    channel_layer = get_channel_layer()
    async_to_sync(channel_layer.group_send)(
        "placar",
        {
            'type': 'send_score',
            'score': {
                'team_a': team_match_a.team.name,
                'team_b': team_match_b.team.name,
                'points_a': point_a,
                'points_b': point_b,
            },
        }
    )
