import psycopg2
from openpyxl import load_workbook
from config import DATABASE_CONFIG
import math
import logging

# Set up logging to a file
logging.basicConfig(filename='elo_log.txt', level=logging.DEBUG, format='%(asctime)s %(levelname)s %(message)s')


# Connect to the database
conn = psycopg2.connect(
    host=DATABASE_CONFIG['host'],
    database=DATABASE_CONFIG['database'],
    user=DATABASE_CONFIG['user'],
    password=DATABASE_CONFIG['password']
)
print("Connected to the database!")


# Create a cursor
cur = conn.cursor()

# Load the workbook
wb = load_workbook('data.xlsx')

# Select the active sheet
ws = wb.active
print("Connected to the XLS sheet!")

def get_player_match_id_by_timestamp_and_by_player_id(player1_id, player2_id, player3_id, player4_id, date, cur):
        cur.execute("SELECT PlayerMatch.player_match_id FROM Match JOIN PlayerMatch ON Match.match_id = PlayerMatch.match_id WHERE PlayerMatch.player_id = %s AND Match.match_timestamp =%s;", (player1_id, date))
        player1_match_id = cur.fetchone()[0]

        cur.execute("SELECT PlayerMatch.player_match_id FROM Match JOIN PlayerMatch ON Match.match_id = PlayerMatch.match_id WHERE PlayerMatch.player_id = %s AND Match.match_timestamp =%s;", (player2_id, date))
        player2_match_id = cur.fetchone()[0]

        cur.execute("SELECT PlayerMatch.player_match_id FROM Match JOIN PlayerMatch ON Match.match_id = PlayerMatch.match_id WHERE PlayerMatch.player_id = %s AND Match.match_timestamp =%s;", (player3_id, date))
        player3_match_id = cur.fetchone()[0]

        cur.execute("SELECT PlayerMatch.player_match_id FROM Match JOIN PlayerMatch ON Match.match_id = PlayerMatch.match_id WHERE PlayerMatch.player_id = %s AND Match.match_timestamp =%s;", (player4_id, date))
        player4_match_id = cur.fetchone()[0]

        return (player1_match_id, player2_match_id, player3_match_id, player4_match_id)

def get_team_match_id_by_timestamp_and_by_team_id(team1_id,team2_id, date, cur):
        cur.execute("SELECT TeamMatch.team_match_id FROM Match JOIN TeamMatch ON Match.match_id = TeamMatch.match_id WHERE TeamMatch.team_id =%s AND Match.match_timestamp =%s;", (team1_id,date))
        team_match1_id = cur.fetchone()[0]

        cur.execute("SELECT TeamMatch.team_match_id FROM Match JOIN TeamMatch ON Match.match_id = TeamMatch.match_id WHERE TeamMatch.team_id =%s AND Match.match_timestamp =%s;", (team2_id,date))
        team_match2_id = cur.fetchone()[0]
        return (team_match1_id,team_match2_id)




# Get the player ID of the players playing a match
def get_player_id(player1_name, player2_name, player3_name, player4_name, cur):
        cur.execute("SELECT player_id FROM player WHERE first_name=%s", (player1_name,))
        player1_id = cur.fetchone()[0]
        logging.info('Processing player1 %s with id %s', player1_name, player1_id)



        cur.execute("SELECT player_id FROM player WHERE first_name=%s", (player2_name,))
        player2_id = cur.fetchone()[0]
        logging.info('Processing player2 %s with id %s', player2_name, player2_id)


        cur.execute("SELECT player_id FROM player WHERE first_name=%s", (player3_name,))
        player3_id = cur.fetchone()[0]
        logging.info('Processing player3 %s with id %s', player3_name, player3_id)

        cur.execute("SELECT player_id FROM player WHERE first_name=%s", (player4_name,))
        player4_id = cur.fetchone()[0]
        logging.info('Processing player4 %s with id %s', player4_name, player4_id)


        # Return a tuple containing all the player IDs
        return (player1_id, player2_id, player3_id, player4_id)

# Get the team ID of the teams playing a match
def insert_team_or_get_team_id(player1_id, player2_id, player3_id, player4_id, cur):
     # Check if the first team already exists
        cur.execute("SELECT team_id FROM team WHERE (team_player_1_id=%s AND team_player_2_id=%s) OR (team_player_1_id=%s AND team_player_2_id=%s)", (player1_id, player2_id, player2_id, player1_id))
        team1_id = cur.fetchone()
        if team1_id is None:
            # If the team does not exist, insert them into the teams table with a unique id
            cur.execute("SELECT nextval('team_id_seq')")
            id = cur.fetchone()[0]
            cur.execute("INSERT INTO team (team_id, team_player_1_id, team_player_2_id) VALUES (%s, %s, %s)", (id, player1_id, player2_id))
            team1_id = id
        else:
            # If the team already exists, retrieve their id
            team1_id = team1_id[0]


        # Check if the second team already exists
        cur.execute("SELECT team_id FROM team WHERE (team_player_1_id=%s AND team_player_2_id=%s) OR (team_player_1_id=%s AND team_player_2_id=%s)", (player3_id, player4_id, player4_id, player3_id))
        team2_id = cur.fetchone()
        if team2_id is None:
            # If the team does not exist, insert them into the teams table with a unique id
            cur.execute("SELECT nextval('team_id_seq')")
            id = cur.fetchone()[0]
            cur.execute("INSERT INTO team (team_id, team_player_1_id, team_player_2_id) VALUES (%s, %s, %s)", (id, player3_id, player4_id))
            team2_id = id

        else:
            # If the team already exists, retrieve their id
            team2_id = team2_id[0]

        # Return the team player IDs as a tuple
        return (team1_id, team2_id)         

def number_of_games_player(player1_id, player2_id, player3_id, player4_id, date, cur):
    cur.execute("SELECT COUNT(*) FROM PlayerMatch pm  INNER JOIN Match m ON pm.match_id = m.match_id  WHERE pm.player_id =%s AND m.match_timestamp <=%s;", (player1_id, date))
    number_of_game_player1 = cur.fetchone()[0] or 0
    logging.info(f'number of game for player {player1_name} on the {date} is {number_of_game_player1}')


    cur.execute("SELECT COUNT(*) FROM PlayerMatch pm  INNER JOIN Match m ON pm.match_id = m.match_id  WHERE pm.player_id =%s AND m.match_timestamp <=%s;", (player2_id, date))
    number_of_game_player2 = cur.fetchone()[0] or 0
    logging.info(f'number of game for player {player2_name} on the {date} is {number_of_game_player2}')

    cur.execute("SELECT COUNT(*) FROM PlayerMatch pm  INNER JOIN Match m ON pm.match_id = m.match_id  WHERE pm.player_id =%s AND m.match_timestamp <=%s;", (player3_id, date))
    number_of_game_player3 = cur.fetchone()[0] or 0
    logging.info(f'number of game for player {player3_name} on the {date} is {number_of_game_player3}')

    cur.execute("SELECT COUNT(*) FROM PlayerMatch pm  INNER JOIN Match m ON pm.match_id = m.match_id  WHERE pm.player_id =%s AND m.match_timestamp <=%s;", (player4_id, date))
    number_of_game_player4 = cur.fetchone()[0] or 0
    logging.info(f'number of game for player {player4_name} on the {date} is {number_of_game_player4}')

    # Return the number of games played by each player as a tuple
    return (number_of_game_player1, number_of_game_player2, number_of_game_player3, number_of_game_player4)


def number_of_games_team(team1_id, team2_id,date, cur):
    cur.execute("SELECT COUNT(*) FROM Match  WHERE winning_team_id =%s OR losing_team_id = %s AND match_timestamp <=%s", (team1_id,team1_id,date))
    number_of_game_team_1 = cur.fetchone()[0] or 0 
    logging.info(f'number of game for team {team1_id} on the {date} is {number_of_game_team_1}')

    cur.execute("SELECT COUNT(*) FROM Match  WHERE winning_team_id =%s OR losing_team_id = %s AND match_timestamp <=%s", (team2_id,team2_id,date))
    number_of_game_team_2 = cur.fetchone()[0] or 0
    logging.info(f'number of game for team {team2_id} on the {date} is {number_of_game_team_2}')
    
     # Return the number of games played by each team as a tuple
    return (number_of_game_team_1, number_of_game_team_2)
             
def get_player_ratings(player1_id, player2_id, player3_id, player4_id, cur):
    cur.execute("SELECT rating, player_rating_timestamp FROM playerrating WHERE player_match_id IN (SELECT player_match_id FROM playermatch WHERE player_id = %s) ORDER BY player_rating_timestamp DESC LIMIT 1;", (player1_id,))

    result = cur.fetchone()
    if result is not None:
        player1_rating = result[0]
    else:
     player1_rating = 1200

    logging.info(f'current rating of player {player1_name} is {player1_rating}')

    cur.execute("SELECT rating, player_rating_timestamp FROM playerrating WHERE player_match_id IN (SELECT player_match_id FROM playermatch WHERE player_id = %s) ORDER BY player_rating_timestamp DESC LIMIT 1;", (player2_id,))
    result = cur.fetchone()
    if result is not None:
        player2_rating = result[0]
    else:
     player2_rating = 1200
    logging.info(f'current rating of player {player2_name} is {player2_rating}')

    cur.execute("SELECT rating, player_rating_timestamp FROM playerrating WHERE player_match_id IN (SELECT player_match_id FROM playermatch WHERE player_id = %s) ORDER BY player_rating_timestamp DESC LIMIT 1;", (player3_id,))
    result = cur.fetchone()
   
    if result is not None:
        player3_rating = result[0]
    else:
     player3_rating = 1200
    logging.info(f'current rating of player {player3_name} is {player3_rating}')

    cur.execute("SELECT rating, player_rating_timestamp FROM playerrating WHERE player_match_id IN (SELECT player_match_id FROM playermatch WHERE player_id = %s) ORDER BY player_rating_timestamp DESC LIMIT 1;", (player4_id,))
    result = cur.fetchone()
    if result is not None:
        player4_rating = result[0]
    else:
        player4_rating = 1200   
    logging.info(f'current rating of player {player4_name} is {player4_rating}')

    return player1_rating, player2_rating, player3_rating, player4_rating


def get_team_ratings(team1_id, team2_id, cur):
    cur.execute("SELECT rating, team_rating_timestamp FROM teamrating WHERE team_match_id IN (SELECT team_match_id FROM teammatch WHERE team_id = %s) ORDER BY team_rating_timestamp DESC LIMIT 1;", (team1_id,))
    result = cur.fetchone()
    
    if result is not None:
        team1_rating = result[0]
    else:
     team1_rating = 1200
    logging.info(f'current rating of team {team1_id} is {team1_rating}')

    cur.execute("SELECT rating, team_rating_timestamp FROM teamrating WHERE team_match_id IN (SELECT team_match_id FROM teammatch WHERE team_id = %s) ORDER BY team_rating_timestamp DESC LIMIT 1;", (team2_id,))
    result = cur.fetchone()
    if result is not None:
        team2_rating = result[0]
    else:
     team2_rating = 1200
    logging.info(f'current rating of team {team2_id} is {team2_rating}')

    return team1_rating, team2_rating


def calculate_point_factor(score_difference):
    return 1 + (math.log(score_difference + 1) / math.log(10)) ** 2




# Iterate through the rows of the sheet
for row in ws.rows:

    # checking if the rows are not null
    if all(cell.value == None for cell in row):
        break
    date = row[0].value
    player1_name = row[1].value
    player2_name = row[2].value
    team1_score = row[3].value
    player3_name = row[4].value
    player4_name = row[5].value
    team2_score = row[6].value

    logging.info('Processing match %s', date)
    
    # Call the get_player_id function inside the loop
    player1_id, player2_id, player3_id, player4_id = get_player_id(player1_name, player2_name, player3_name, player4_name, cur)

    # Call the insert_team_or_get_team_id function inside the loop
    team1_id, team2_id = insert_team_or_get_team_id(player1_id, player2_id, player3_id, player4_id, cur)

    # Call the number_of_games_player function inside the loop
    number_of_game_player1, number_of_game_player2, number_of_game_player3, number_of_game_player4 = number_of_games_player(player1_id, player2_id, player3_id, player4_id, date, cur)

    # Call the number_of_games_team function inside the loop
    number_of_games_team1, number_of_games_team2 = number_of_games_team(team1_id, team2_id, date, cur)

    # Call the get_player_ratings function inside the loop
    player1_rating, player2_rating, player3_rating, player4_rating = get_player_ratings(player1_id, player2_id, player3_id, player4_id, cur)

    # Call the get_teams_ratings function inside the loop
    team1_rating, team2_rating = get_team_ratings(team1_id, team2_id, cur)

    # Call the get_player_match_id_by_timestamp_and_by_player_id function inside the loop
    player_match1_id, player_match2_id, player_match3_id, player_match4_id  = get_player_match_id_by_timestamp_and_by_player_id(player1_id, player2_id, player3_id, player4_id, date, cur)

    # Call the get_team_match_id_by_timestamp_and_by_team_id function inside the loop
    team_match1_id, team_match2_id  = get_team_match_id_by_timestamp_and_by_team_id(team1_id, team2_id, date, cur)

    
    # Calculate the expected scores for the players
    player1_expected_score_against_player3 = 1 / (1 + 10**((player3_rating - player1_rating) / 400))
    player1_expected_score_against_player4 = 1 / (1 + 10**((player4_rating - player1_rating) / 400))
    player1_expected_score = (player1_expected_score_against_player3 + player1_expected_score_against_player4) / 2
    logging.info('Player %s expected score against player %s: %s',player1_name, player3_name, player1_expected_score_against_player3)
    logging.info('Player %s expected score against player %s: %s', player1_name, player4_name,player1_expected_score_against_player4)
    logging.info('Player %s overall expected score: %s',player1_name, player1_expected_score)

    player2_expected_score_against_player3 = 1 / (1 + 10**((player3_rating - player2_rating) / 400))
    player2_expected_score_against_player4 = 1 / (1 + 10**((player4_rating - player2_rating) / 400))
    player2_expected_score = (player2_expected_score_against_player3 + player2_expected_score_against_player4) / 2
    logging.info('Player %s expected score against player %s: %s',player2_name, player3_name, player2_expected_score_against_player3)
    logging.info('Player %s expected score against player %s: %s', player2_name, player4_name,player2_expected_score_against_player4)
    logging.info('Player %s overall expected score: %s',player2_name, player2_expected_score)

    player3_expected_score_against_player1 = 1 / (1 + 10**((player1_rating - player3_rating) / 400))
    player3_expected_score_against_player2 = 1 / (1 + 10**((player2_rating - player3_rating) / 400))
    player3_expected_score = (player3_expected_score_against_player1 + player3_expected_score_against_player2) / 2
    logging.info('Player %s expected score against player %s: %s',player3_name, player1_name, player3_expected_score_against_player1)
    logging.info('Player %s expected score against player %s: %s', player3_name, player2_name,player3_expected_score_against_player2)
    logging.info('Player %s overall expected score: %s',player3_name, player3_expected_score)

    player4_expected_score_against_player1 = 1 / (1 + 10**((player1_rating - player4_rating) / 400))
    player4_expected_score_against_player2 = 1 / (1 + 10**((player2_rating - player4_rating) / 400))
    player4_expected_score = (player4_expected_score_against_player1 + player4_expected_score_against_player2) / 2
    logging.info('Player %s expected score against player %s: %s',player4_name, player1_name, player4_expected_score_against_player1)
    logging.info('Player %s expected score against player %s: %s', player4_name, player2_name,player4_expected_score_against_player2)
    logging.info('Player %s overall expected score: %s',player4_name, player4_expected_score)

    #input("Press enter to continue...")

    # Calculate the expected scores for the teams
    team1_expected_score = (player1_expected_score + player2_expected_score) / 2
    team2_expected_score = (player3_expected_score + player4_expected_score) / 2

    logging.info("Team 1 expected score: %s", team1_expected_score)
    logging.info("Team 2 expected score: %s", team2_expected_score)
    #input("Press enter to continue...")

    # Calculate the score difference to be used as a variable
    team1_actual_score = team1_score / (team1_score + team2_score)* 1.025
    team2_actual_score = team2_score / (team1_score + team2_score) *1.025

    logging.info("Team 1 actual score: %s", team1_actual_score)
    logging.info("Team 2 actual score: %s", team2_actual_score)

    #input("Press enter to continue...")


    # Calculate the point factor to be used as a variable
    score_difference = abs(team1_score - team2_score)
    point_factor = calculate_point_factor(score_difference)
    logging.info("Point factor: %s", point_factor)


   #input("Press enter to continue...")

     # Calculate the K value for each player based on the number of games played and their rating
    k1 = 300 / (1 + number_of_game_player1 / 500) * (2200 - player1_rating) / 1000
    k2 = 300 / (1 + number_of_game_player2 / 500) * (2200 - player2_rating) / 1000
    k3 = 300 / (1 + number_of_game_player3 / 500) * (2200 - player3_rating) / 1000
    k4 = 300 / (1 + number_of_game_player4 / 500) * (2200 - player4_rating) / 1000

    logging.info('Player %s K value: %s', player1_name,k1)
    logging.info('Player %s K value: %s', player2_name,k2)
    logging.info('Player %s K value: %s', player3_name,k3)
    logging.info('Player %s K value: %s', player4_name,k4)


    # Calculate the K value for each team based on the number of games played
    k5 = 50 / (1 + number_of_games_team1/ 200)
    k6 = 50 / (1 + number_of_games_team2/ 200)

    logging.info('Team %s K value: %s', team1_id,k5)
    logging.info('Team %s K value: %s', team2_id,k6)

   #input("Press enter to continue...")

 #logg the wining team
    if team1_score > team2_score:
       
        logging.info('team 1 win with %s and : %s', player1_name,player2_name)
        logging.info('team 2 lost with %s and : %s', player3_name,player4_name)

    else:
        logging.info('team 1 lost with %s and : %s', player1_name,player2_name)
        logging.info('team 2 win with %s and : %s', player3_name,player4_name)
        

    # Calculate the new Elo ratings for each player
    player1_new_rating = player1_rating + k1 * point_factor * (team1_actual_score - player1_expected_score)
    player2_new_rating = player2_rating + k2 * point_factor * (team1_actual_score - player2_expected_score)
    player3_new_rating = player3_rating + k3 * point_factor * (team2_actual_score - player3_expected_score)
    player4_new_rating = player4_rating + k4 * point_factor * (team2_actual_score - player4_expected_score)
    
    # Log the new ratings
    logging.info('%s new rating: %s = %s + %s * %s * (%s - %s)', player1_name, player1_new_rating, player1_rating, k1, point_factor, team1_actual_score, player1_expected_score)
    logging.info('%s new rating: %s = %s + %s * %s * (%s - %s)', player2_name, player2_new_rating, player2_rating, k2, point_factor, team1_actual_score, player2_expected_score)
    logging.info('%s new rating: %s = %s + %s * %s * (%s - %s)', player3_name, player3_new_rating, player3_rating, k3, point_factor, team2_actual_score, player3_expected_score)
    logging.info('%s new rating: %s = %s + %s * %s * (%s - %s)', player4_name, player4_new_rating, player4_rating, k4, point_factor, team2_actual_score, player4_expected_score)



    #input("Press enter to continue...")

    # Calculate the new Elo ratings for each team
    team1_new_rating = team1_rating + k5 * point_factor * (team1_actual_score - team1_expected_score)
    team2_new_rating = team2_rating + k6 * point_factor * (team2_actual_score - team2_expected_score)
    # Log the new ratings for teams
    logging.info('Team 1 new rating: %s = %s + %s * %s * (%s - %s)', team1_new_rating, team1_rating, k5, point_factor, team1_actual_score, team1_expected_score)
    logging.info('Team 2 new rating: %s = %s + %s * %s * (%s - %s)', team2_new_rating, team2_rating, k6, point_factor, team2_actual_score, team2_expected_score)


    #input("Press enter to continue...")

    
    # Update the database with the player ratings
    cur.execute("INSERT INTO playerrating (player_match_id, rating, player_rating_timestamp) VALUES (%s, %s, %s)", (player_match1_id, player1_new_rating, date))
    cur.execute("INSERT INTO playerrating (player_match_id, rating, player_rating_timestamp) VALUES ( %s, %s, %s)", (player_match2_id, player2_new_rating, date))
    cur.execute("INSERT INTO playerrating (player_match_id,rating, player_rating_timestamp) VALUES (%s, %s, %s)", (player_match3_id,player3_new_rating, date))
    cur.execute("INSERT INTO playerrating (player_match_id, rating, player_rating_timestamp) VALUES (%s, %s, %s)", (player_match4_id, player4_new_rating, date))
    conn.commit()

    # Update the database with the team ratings
    cur.execute("INSERT INTO teamrating (team_match_id, rating, team_rating_timestamp) VALUES (%s, %s, %s)", (team_match1_id, team1_new_rating, date))
    cur.execute("INSERT INTO teamrating (team_match_id, rating, team_rating_timestamp) VALUES (%s, %s, %s)", (team_match2_id, team2_new_rating, date))
    conn.commit()


# Close the cursor and connection
cur.close()
conn.close()