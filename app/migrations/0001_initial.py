# Generated by Django 5.1.1 on 2024-10-15 18:07

import django.core.validators
import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Player',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('instagram', models.CharField(blank=True, max_length=100)),
                ('photo', models.ImageField(blank=True, default='defaults/profile_default.png', upload_to='photo_player/')),
                ('sexo', models.IntegerField(choices=[(0, 'Masculino'), (1, 'Feminino'), (2, 'Nenhum')], default=2)),
            ],
        ),
        migrations.CreateModel(
            name='Sport',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('max_titulares', models.IntegerField(validators=[django.core.validators.MaxValueValidator(50)])),
            ],
        ),
        migrations.CreateModel(
            name='Team',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, max_length=100)),
                ('photo', models.ImageField(blank=True, default='defaults/team_default.png', upload_to='logo_team/')),
                ('hexcolor', models.CharField(max_length=6, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Match',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.IntegerField(choices=[(0, 'Em breve'), (1, 'Acontecendo'), (2, 'Finalizada'), (3, 'Cancelada'), (4, 'Pausada'), (5, 'Nenhum')], default=5)),
                ('time_start', models.TimeField(blank=True, null=True)),
                ('time_end', models.TimeField(blank=True, null=True)),
                ('sexo', models.IntegerField(blank=True, choices=[(0, 'Masculino'), (1, 'Feminino'), (2, 'Nenhum')], default=2)),
                ('add', models.TimeField(blank=True, null=True)),
                ('time_match', models.DateTimeField(blank=True, null=True)),
                ('mvp_player_player', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='app.player')),
                ('sport', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.sport')),
                ('Winner_team', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='app.team')),
            ],
        ),
        migrations.CreateModel(
            name='Player_match',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('player_number', models.IntegerField(blank=True, default=0, null=True)),
                ('activity', models.IntegerField(choices=[(0, 'Titular'), (1, 'Reserva'), (2, 'Nenhum')], default=2)),
                ('match', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.match')),
                ('player', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.player')),
            ],
        ),
        migrations.CreateModel(
            name='Point',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('point_types', models.IntegerField(choices=[(0, 'Gol'), (1, 'Ponto'), (2, 'Ace'), (3, 'Nenhum')], default=3)),
                ('time', models.TimeField()),
                ('player', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.player')),
            ],
        ),
        migrations.CreateModel(
            name='Assistance',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('player', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.player')),
                ('assis_to', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.point')),
            ],
        ),
        migrations.CreateModel(
            name='Team_match',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('match', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.match')),
                ('team', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.team')),
            ],
        ),
        migrations.AddField(
            model_name='point',
            name='team_match',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.team_match'),
        ),
        migrations.CreateModel(
            name='Penalties',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('type_penalties', models.IntegerField(choices=[(0, 'Cartão Vermelho'), (1, 'Cartão Amarelo'), (2, 'Nenhum')], default=2)),
                ('time', models.TimeField()),
                ('player', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.player')),
                ('team_match', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.team_match')),
            ],
        ),
        migrations.CreateModel(
            name='Team_sport',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sport', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.sport')),
                ('team', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.team')),
            ],
        ),
        migrations.CreateModel(
            name='Player_team_sport',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('player', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.player')),
                ('team_sport', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.team_sport')),
            ],
        ),
        migrations.CreateModel(
            name='time_pause',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('start_pause', models.TimeField()),
                ('end_pause', models.TimeField()),
                ('match', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.match')),
            ],
        ),
        migrations.CreateModel(
            name='Volley_match',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.IntegerField(choices=[(0, 'Em breve'), (1, 'Acontecendo'), (2, 'Finalizada'), (3, 'Cancelada'), (4, 'Pausada'), (5, 'Nenhum')], default=5)),
                ('sets_team', models.IntegerField(default=0)),
                ('team_match', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.team_match')),
            ],
        ),
        migrations.AddField(
            model_name='match',
            name='volley_match',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='app.volley_match'),
        ),
    ]
