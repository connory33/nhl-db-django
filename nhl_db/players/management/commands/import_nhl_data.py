# players/management/commands/import_nhl_data.py
from django.core.management.base import BaseCommand
import psycopg2
from players.models import Player, Team

class Command(BaseCommand):
    help = 'Import NHL data from existing PostgreSQL database'

    def handle(self, *args, **kwargs):
        # Connect to your existing database
        source_conn = psycopg2.connect(
            dbname='your_old_db',
            user='your_db_user',
            password='your_db_password',
            host='localhost'
        )
        source_cursor = source_conn.cursor()
        
        # Import teams first
        self.stdout.write('Importing teams...')
        source_cursor.execute('SELECT id, name, triCode, teamLogo FROM nhl_teams')
        teams = source_cursor.fetchall()
        
        for team_data in teams:
            Team.objects.create(
                id=team_data[0],
                name=team_data[1],
                triCode=team_data[2],
                teamLogo=team_data[3]
            )
        
        # Import players
        self.stdout.write('Importing players...')
        source_cursor.execute('''
            SELECT 
                playerId, firstName, lastName, heightInInches, heightInCentimeters, 
                weightInPounds, weightInKilograms, birthDate, birthCountry, 
                shootsCatches, isActive, sweaterNumber, currentTeamID
            FROM nhl_players
        ''')
        players = source_cursor.fetchall()
        
        for player_data in players:
            Player.objects.create(
                playerId=player_data[0],
                firstName=player_data[1],
                lastName=player_data[2],
                heightInInches=player_data[3],
                heightInCentimeters=player_data[4],
                weightInPounds=player_data[5],
                weightInKilograms=player_data[6],
                birthDate=player_data[7],
                birthCountry=player_data[8],
                shootsCatches=player_data[9],
                isActive=player_data[10],
                sweaterNumber=player_data[11],
                currentTeamID_id=player_data[12]
            )
        
        self.stdout.write(self.style.SUCCESS('Successfully imported NHL data'))