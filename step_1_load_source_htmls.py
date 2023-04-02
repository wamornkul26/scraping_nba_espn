from urllib.request import urlopen
from bs4 import BeautifulSoup
from dateutil.parser import parse
import os
import re

# sources are coming from espn.com
# read html and write to file
def load_page_url(url, output_file_name):
    page = urlopen(url)

    html_bytes = page.read()
    html = html_bytes.decode("utf-8")

    f = open(output_file_name, "w")
    f.write(html)
    f.close()
    return html

# load file
def load_file(file_name):
    HTMLFile = open(file_name, "r")
    
    # Reading the file
    html = HTMLFile.read()
    return html

# get team matchup stats
# input: https://www.espn.com/nba/matchup/_/gameId/[401468017]
# output: ./inputs/html/[team]/[season]/nba_[game_id]_boxscore.html 
def get_game_matchup_stats(team, game_id, season, file_path):  
    url = "https://www.espn.com/nba/matchup/_/gameId/" + game_id
    file_name = file_path + "/nba_" + game_id + "_matchup.html"
   
    print('get_game_matchup_stats::file_name - ' + file_name)
    
    # if file exists, then load from local
    if os.path.isfile(file_name):
        print("File does exists, load from file")
        html = load_file(file_name)
    else:
        print("File does not exists, load from web")
        html = load_page_url(url, file_name)

# team boxscore
# input: https://www.espn.com/nba/boxscore/_/gameId/[401468017]
# output: ./inputs/html/[team]/[season]/nba_[game_id]_boxscore.html 
def get_game_boxscore_stats(team, game_id, season, file_path):   
    url = "https://www.espn.com/nba/boxscore/_/gameId/" + game_id
    file_name = file_path + "/nba_" + game_id + "_boxscore.html"

    print('get_game_boxscore_stats::file_name - ' + file_name)
    
    # if file exists, then load from local
    if os.path.isfile(file_name):
        print("File does exists, load from file")
        html = load_file(file_name)
    else:
        print("File does not exists, load from web")
        html = load_page_url(url, file_name)

# Scrape team schedule page
def load_game_data(team, season, html, file_path):
    # parse html content
    soup = BeautifulSoup(html, "html.parser")

    # Load table - schedule only have one table
    tbl = soup.find("table")

    # Open file for appending
    data_rows = tbl.find_all("tr", attrs={'class': re.compile(r'Table__TR Table__TR--sm Table__even')})
    
    for data_row in data_rows[1:]:
        data_str = ''

        # try to split out data
        col = ''
        cols = data_row.find_all("td")
        if len(cols) > 1:
            if cols[2].find("span", class_="ml4") != None:
                link = cols[2].find("span", class_="ml4").a['href']
                game_id = link.split('/')[7]

                get_game_matchup_stats(team, game_id, season, file_path)
                get_game_boxscore_stats(team, game_id, season, file_path)   


# get team schedules page
# input: https://www.espn.com/nba/team/schedule/_/name/[gs]/season/[2023]
# output: ./inputs/html/[team]/[season]/nba_schedule_[season].html 
def get_team_schedule_html(team, season, loadFromWeb):
    season = str(season)
    url = "https://www.espn.com/nba/team/schedule/_/name/" + team + "/season/" + season
    file_path = "./inputs/html/" + team + "/" + season + "/"

    # create file path if does not exist
    if not os.path.exists(file_path):
        print("File path " + file_path + " deos not exists")
        os.makedirs(file_path) 

    print("file_path - " + file_path)
    file_name = file_path + "nba_schedule_" + season + ".html"

    # if file exists, then load from local
    if os.path.isfile(file_name) and not loadFromWeb:
        print("File does exists, load from file")
        html = load_file(file_name)
    else:
        print("File does not exists, load from web")
        html = load_page_url(url, file_name)

    # Load loop through game schedules and load game matchup and boxscore for each game
    load_game_data(team, season, html, file_path)
    print('step_1_load_source_htmls::done') 
