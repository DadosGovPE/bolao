from django.core.management.base import BaseCommand
from bolao.models import *
import pandas as pd

class Command(BaseCommand):
    help = 'Popula a tabela com dados de uma planilha'

    def handle(self, *args, **kwargs):
        df = pd.read_csv('partidas-olimpiadas.csv')
        df['datetime'] = pd.to_datetime(df['Date'] + ' ' + df['Time'], format='%d-%m-%Y %H:%M')
        teams = pd.concat([df['Team1'], df['Team2']])

        # Remover duplicatas
        unique_teams = teams.drop_duplicates().tolist()
        campeonato, created = Campeonato.objects.get_or_create(pk=1, defaults={'nome': 'Olimpíadas 2024'})
        if created:
            print("Campeonato com pk=1 foi criado.")
            
        for time in unique_teams:
            try:
                Team.objects.create(
                name=time
                )
                # Adicione todos os campos que você precisa mapear
            except Exception as e:
                print(f"Erro ao processar a linha {time}. Erro: {e}")
        self.stdout.write(self.style.SUCCESS('Tabela Team populada com sucesso!'))

        
        for index, row in df.iterrows():
            try:
                time1 = Team.objects.get(name=row['Team1'])
                time2 = Team.objects.get(name=row['Team2'])
                Game.objects.create(
                team1=time1,
                team2=time2,
                final_score1=0,
                final_score2=0,
                campeonato=campeonato,
                location=row['Location'],
                fase=row['Fase'],
                date=row['datetime']
                )
                # Adicione todos os campos que você precisa mapear
            except Exception as e:
                print(f"Erro ao processar a linha {index}: {row['Location']}. Erro: {e}")
            
        self.stdout.write(self.style.SUCCESS('Tabela Game populada com sucesso!'))

#Date,Time,Group,Location,Team1,Team2,Fase

# class Game(models.Model):
#     team1 = models.ForeignKey(Team, related_name='team1_games', on_delete=models.CASCADE)
#     team2 = models.ForeignKey(Team, related_name='team2_games', on_delete=models.CASCADE)
#     final_score1 = models.IntegerField()
#     final_score2 = models.IntegerField()
#     campeonato = models.ForeignKey(Campeonato,on_delete=models.CASCADE, blank=False, null=False)
#     location = models.CharField(max_length=100, blank=True, null=True)
#     fase = models.CharField(max_length=100, blank=True, null=True)
#     date = models.DateTimeField()

#     def __str__(self):
#         return f"{self.team1} vs {self.team2} - {self.date}"