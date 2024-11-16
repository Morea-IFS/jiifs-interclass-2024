# app/signals.py
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.conf import settings
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
from .models import Point, Match, Team_match

default_photo_url = f"{settings.MEDIA_URL}defaults/person.png"

@receiver([post_save,post_delete], sender=Point)
def point_removed(sender, instance, using, **kwargs):
    match = Match.objects.get(status=1)
    team_matchs = Team_match.objects.filter(match=match)
    team_match_a = team_matchs[0]
    team_match_b = team_matchs[1]
    point_a = Point.objects.filter(team_match=team_match_a).count()
    point_b = Point.objects.filter(team_match=team_match_b).count()
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
                'photoA': team_match_a.team.photo.url,
                'photoB': team_match_b.team.photo.url,
            },
        }
    )

@receiver(post_save, sender=Match)
def match_status_updated(sender, instance, created, **kwargs):
    if Match.objects.filter(status=1):
        match = Match.objects.get(status=1)
        team_matchs = Team_match.objects.filter(match=match)
        team_match_a = team_matchs[0]
        team_match_b = team_matchs[1] 
        point_a = Point.objects.filter(team_match=team_match_a).count()
        point_b = Point.objects.filter(team_match=team_match_b).count()
        channel_layer = get_channel_layer()
        match_data = {
            'team_a': team_match_a.team.name,
            'team_b': team_match_b.team.name,
            'points_a': point_a,
            'points_b': point_b,
        }
        match_data['photoA'] = team_match_a.team.photo.url if team_match_a.team.photo else default_photo_url
        match_data['photoB'] = team_match_b.team.photo.url if team_match_b.team.photo else default_photo_url

        async_to_sync(channel_layer.group_send)(
            'placar',  # Nome do grupo para enviar a mensagem
            {
                'type': 'match_update',
                'match': match_data,
            }
        )