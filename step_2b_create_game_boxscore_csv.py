from urllib.request import urlopen
from bs4 import BeautifulSoup
from dateutil.parser import parse
from dateutil.relativedelta import relativedelta
import pandas as pd
import os
import re
import csv

# load file
def load_file(file_name):
    HTMLFile = open(file_name, "r")
    
    # Reading the file
    html = HTMLFile.read()
    return html

# get team schedule html page
# input: ./inputs/html/[team]/[season]/nba_schedule_[season].html
# output: html 
def get_team_schedule_html(team, season):
    input_file_path = "./inputs/html/" + team + "/" + season + "/"
    input_file_name = input_file_path + "nba_schedule_" + season + ".html"

    html = load_file(input_file_name)
    return html

# get game matchup html page
# input: ./inputs/html/[team]/[season]/nba_[game_id]_boxscore.html
# output: html
def get_game_boxscore_html(team, season, game_id):
    input_file_path = "./inputs/html/" + team + "/" + season + "/"
    input_file_name = input_file_path + "nba_" + str(game_id) + "_boxscore.html"

    html = load_file(input_file_name)
    return html

# safe divide
def safe_div(x,y):
    if y==0: return 0
    return float(x/y)

def get_team_name(team):
    teams = {
        "bos" : "Boston Celtics",
        "bkn" : "Brooklyn Nets",
        "ny" : "New York Knicks",
        "phi" : "Philadelphia 76ers",
        "tor" : "Toronto Raptors",

        "den" : "Denver Nuggets",
        "min" : "Minnesota Timberwolves",
        "okc" : "Oklahoma City Thunder",
        "por" : "Portland Trail Blazers",
        "utah" : "Utah Jazz",

        "chi" : "Chicago Bulls",
        "cle" : "Cleveland Cavaliers",
        "det" : "Detroit Pistons",
        "ind" : "Indiana Pacers",
        "mil" : "Milwaukee Bucks",

        "gs" : "Golden State Warriors",
        "lac" : "LA Clippers",
        "lal" : "Los Angeles Lakers",
        "phx" : "Phoenix Suns",
        "sac" : "Sacramento Kings",

        "atl" : "Atlanta Hawks",
        "cha" : "Charlotte Hornets",
        "mia" : "Miami Heat",
        "orl" : "Orlando Magic",
        "wsh" : "Washington Wizards",

        "dal" : "Dallas Mavericks",
        "hou" : "Houston Rockets",
        "mem" : "Memphis Grizzlies",
        "no" : "New Orleans Pelicans",
        "sa" : "San Antonio Spurs"
    }

    return teams[team]

def generate_team_boxscore_csv(team, season):
    season = str(season)

    output_file_path = "./outputs/csv/" + team + "/" + season + "/"
    input_file_name = output_file_path + "nba_" + team + "_schedule_" + season + ".csv"
    output_file_name = output_file_path + "nba_" + team + "_boxscore_" + season + ".csv"

    # load csv to schedule dataframe
    schedule_df = pd.read_csv(input_file_name)

    boxscore_list = []

    # loop through the schedule dataframe and process each game boxscore
    for index, row in schedule_df.iterrows():
        row['game_id'] = str(int(row['game_id']))
        # get the game boxscore
        html = get_game_boxscore_html(team, season, row['game_id'])

        # parse html content
        soup = BeautifulSoup(html, "html.parser")

        boxscores = soup.find_all("div", class_="Boxscore flex flex-column")

        # determine if the team score is on the left or right
        team_loc = 0

        if boxscores[1].img['alt'] == get_team_name(team):
            team_loc = 1

        tables = boxscores[team_loc].find_all("table")
        td0s = tables[0].find_all("td")
        play_group = ""

        # the user column is separate from data, we want to capture name and lineup
        line_up = []
        players = []
        for td in td0s:
            if td.text == "starters" or td.text == "bench":
                play_group = td.text
            elif td.text == "team":
                break;             
            else:
                line_up.append(play_group)
                players.append(td.text)

        # now loop through the data table
        data_rows = tables[1].tbody.find_all("tr")
        row_count = 0
        for data_row in data_rows[1:]:
            data_cols = data_row.find_all("td", class_="Table__TD Table__TD")

            if ((row_count + 4) == len(data_rows)):
                break

            # this is to get position
            names_list = players[row_count].rsplit(" ", 1)
 
            player_dict = { 
                'game_id': row['game_id'], 'season': season, 'game_date': row['game_date'], 
                'line_up' : line_up[row_count], 'player' : names_list[0], 'result': row['result'], 
                'pos' : names_list[1], 'home_game' : row['home_game'], 'opponent' : row['opponent'] }

            if (len(data_cols) > 1):
                player_dict['min'] = int(data_cols[0].text) if data_cols[0].text else 0

                fg = data_cols[1].text.split("-")
                
                player_dict['fg_made'] = int(fg[0]) if fg[0] else 0
                player_dict['fg_attempt'] = int(fg[1]) if fg[1] else 0
                player_dict['fg_pct'] = safe_div(int(fg[0]), int(fg[1]))

                three_pt = data_cols[2].text.split("-")
                player_dict['three_pt_made'] = int(three_pt[0]) if three_pt[0] else 0
                player_dict['three_pt_attempt'] = int(three_pt[1]) if three_pt[1] else 0
                player_dict['three_pt_pct'] = safe_div(int(three_pt[0]), int(three_pt[1]))

                ft = data_cols[3].text.split("-")
                player_dict['ft_made'] = int(ft[0]) if ft[0] else 0
                player_dict['ft_attempt'] = int(ft[1]) if ft[1] else 0
                player_dict['ft_pct'] = safe_div(int(ft[0]), int(ft[1]))

                player_dict['oreb'] = int(data_cols[4].text) if data_cols[4].text else 0
                player_dict['dreb'] = int(data_cols[5].text) if data_cols[5].text else 0
                player_dict['reb'] = int(data_cols[6].text) if data_cols[6].text else 0
                player_dict['ast'] = int(data_cols[7].text) if data_cols[7].text else 0
                player_dict['stl'] = int(data_cols[8].text) if data_cols[8].text else 0
                player_dict['blk'] = int(data_cols[9].text) if data_cols[9].text else 0
                player_dict['to'] = int(data_cols[10].text) if data_cols[10].text else 0
                player_dict['pf'] = int(data_cols[11].text) if data_cols[11].text else 0
                player_dict['plus_minus'] = int(data_cols[12].text) if data_cols[12].text else 0
                player_dict['pts'] = int(data_cols[13].text) if data_cols[13].text else 0
                
                boxscore_list.insert(row_count, player_dict)
                row_count = row_count + 1  

    # write to output file
    f = open(output_file_name, "w")
    writer = csv.writer(f)
    
    # get header (dictionary keys)
    sample_dict = boxscore_list[0]
    writer.writerow(sample_dict.keys())

    for dictionary in boxscore_list:
        writer.writerow(dictionary.values())
    f.close()

    print('step_2b_create_team_boxscore_csv::done')
