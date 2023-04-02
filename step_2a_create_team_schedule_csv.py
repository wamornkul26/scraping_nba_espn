from urllib.request import urlopen
from bs4 import BeautifulSoup
from dateutil.parser import parse
from dateutil.relativedelta import relativedelta
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
# input: ./inputs/html/[team]/[season]/nba_[game_id]_matchup.html
# output: html 
def get_game_matchup_html(team, season, game_id):
    input_file_path = "./inputs/html/" + team + "/" + season + "/"
    input_file_name = input_file_path + "nba_" + game_id + "_matchup.html"

    html = load_file(input_file_name)
    return html

def get_team_stat(data_cols, team_col, opp_team_col, game_dict):
    if data_cols[0].text == "FG":
        fg = data_cols[team_col].text.split("-")
        game_dict['fg_made'] = int(fg[0])
        game_dict['fg_attempt'] = int(fg[1]) 
        ofg = data_cols[opp_team_col].text.split("-")
        game_dict['opp_fg_made'] = int(ofg[0])
        game_dict['opp_fg_attempt'] = int(ofg[1])            
    elif data_cols[0].text == "Field Goal %":
        game_dict['fg_pct'] = float(data_cols[team_col].text)
        game_dict['opp_fg_pct'] = float(data_cols[opp_team_col].text)
    elif data_cols[0].text == "3PT":
        threept = data_cols[team_col].text.split("-")
        game_dict['three_pt_made'] = int(threept[0])
        game_dict['three_pt_attempt'] = int(threept[1])
        othreept = data_cols[opp_team_col].text.split("-")
        game_dict['opp_three_pt_made'] = int(othreept[0])
        game_dict['opp_three_pt_attempt'] = int(othreept[1])        
    elif data_cols[0].text == "Three Point %":       
        game_dict['three_pt_pct'] = float(data_cols[team_col].text)
        game_dict['opp_three_pt_pct'] = float(data_cols[opp_team_col].text)
    elif data_cols[0].text == "FT":
        ft = data_cols[team_col].text.split("-")
        game_dict['ft_made'] = int(ft[0])
        game_dict['ft_attempt'] = int(ft[1])
        oft = data_cols[opp_team_col].text.split("-")
        game_dict['opp_ft_made'] = int(oft[0])
        game_dict['opp_ft_attempt'] = int(oft[1])        
    elif data_cols[0].text == "Free Throw %":        
        game_dict['ft_pct'] = float(data_cols[team_col].text)
        game_dict['opp_ft_pct'] = float(data_cols[opp_team_col].text)
    elif data_cols[0].text == "Rebounds":
        game_dict['rebs'] = int(data_cols[team_col].text)
        game_dict['opp_rebs'] = int(data_cols[opp_team_col].text)
    elif data_cols[0].text == "Offensive Rebounds":
        game_dict['off_rebs'] = int(data_cols[team_col].text)
        game_dict['opp_off_rebs'] = int(data_cols[opp_team_col].text)
    elif data_cols[0].text == "Defensive Rebounds":
        game_dict['def_rebs'] = int(data_cols[team_col].text)
        game_dict['opp_def_rebs'] = int(data_cols[opp_team_col].text)
    elif data_cols[0].text == "Assists":
        game_dict['assts'] = int(data_cols[team_col].text)
        game_dict['opp_assts'] = int(data_cols[opp_team_col].text)
    elif data_cols[0].text == "Steals":
        game_dict['stls'] = int(data_cols[team_col].text)
        game_dict['opp_stls'] = int(data_cols[opp_team_col].text)
    elif data_cols[0].text == "Blocks":
        game_dict['blks'] = int(data_cols[team_col].text)
        game_dict['opp_blks'] = int(data_cols[opp_team_col].text)
    elif data_cols[0].text == "Total Turnovers":
        game_dict['total_tovs'] = int(data_cols[team_col].text)
        game_dict['opp_total_tovs'] = int(data_cols[opp_team_col].text)
    elif data_cols[0].text == "Points Off Turnovers":
        game_dict['pts_of_tovs'] = int(data_cols[team_col].text)
        game_dict['opp_pts_of_tovs'] = int(data_cols[opp_team_col].text)
    elif data_cols[0].text == "Fast Break Points":
        game_dict['fastbrk_pts'] = int(data_cols[team_col].text)
        game_dict['opp_fastbrk_pts'] = int(data_cols[opp_team_col].text)
    elif data_cols[0].text == "Points in Paint":
        game_dict['pts_in_paint'] = int(data_cols[team_col].text)
        game_dict['opp_pts_in_paint'] = int(data_cols[opp_team_col].text)
    elif data_cols[0].text == "Fouls":
        game_dict['fls'] = int(data_cols[team_col].text)
        game_dict['opp_fls'] = int(data_cols[opp_team_col].text)
    elif data_cols[0].text == "Technical Fouls":
        game_dict['tech_fls'] = int(data_cols[team_col].text)
        game_dict['opp_tech_fls'] = int(data_cols[opp_team_col].text)
    elif data_cols[0].text == "Flagrant Fouls":
        game_dict['flg_fls'] = int(data_cols[team_col].text)
        game_dict['opp_flg_fls'] = int(data_cols[opp_team_col].text)
    elif data_cols[0].text == "Largest Lead":
        game_dict['largest_lead'] = int(data_cols[team_col].text)
        game_dict['opp_largest_lead'] = int(data_cols[opp_team_col].text)

def get_game_matchup_data(team, season, game_id, game_dict):
    # get html
    html = get_game_matchup_html(team, season, game_id)

    # parse html content
    soup = BeautifulSoup(html, "html.parser")

    teams = soup.find_all("div", class_="Gamestrip__Team")
    team_col = 1
    opp_team_col = 1
    if teams[1].a['href'].split('/')[5] == team:
        team_col = 2
    else:
        opp_team_col = 2

    # Load table
    tbl = soup.find("section", class_="Card TeamStatsTable")

    # Get Body
    body_data = tbl.find("tbody", class_="Table__TBODY")
    data_rows = body_data.find_all("tr")

    for data_row in data_rows:
        data_cols = data_row.find_all("td")
        get_team_stat(data_cols, team_col, opp_team_col, game_dict)


def generate_team_schedule_csv(team, season):
    season = str(season)

    output_file_path = "./outputs/csv/" + team + "/" + season + "/"
    output_file_name = output_file_path + "nba_" + team + "_schedule_" + season + ".csv"

    # create file path if does not exist
    if not os.path.exists(output_file_path):
        print("File " + output_file_path + " deos not exists")
        os.makedirs(output_file_path) 

    print("generate_team_schedule_csv")

    # load team schedule html file
    html = get_team_schedule_html(team, season)

    # parse html content with BeautifulSoup
    soup = BeautifulSoup(html, "html.parser")

    # Load table - schedule only have one table
    tbl = soup.find("table")

    # load data rows
    data_rows = soup.find_all("tr", attrs={'class': re.compile(r'Table__TR Table__TR--sm Table__even')})
    game_list = []

    season_year = int(season) - 1
    for data_row in data_rows[1:]:
        game_dict = {}

        # try to split out data
        cols = data_row.find_all("td")
        if len(cols) > 1:
            # col 0 is date
            if cols[0].span.text == "DATE":
                break
            
            game_dict["season"] = season

            dt = parse(cols[0].span.text + ' ' + str(season_year))
            if dt.month == 1 and season_year < int(season):
                season_year = season_year + 1
                new_dt = dt + relativedelta(years=1)
                game_dict["game_date"] = new_dt
            else:
                game_dict["game_date"] = dt

            # col 1 is home/away and opponent
            loc = 'Y'
            if cols[1].div.span.text == "@":
                loc = 'N'
            game_dict["home_game"] = str(loc)
            game_dict["opponent"] = cols[1].img['title']

            # col 2 is result, score, and opponent_score
            status = "-"
            if cols[2].text == "Postponed":
                # status = cols[2].text
                continue
            elif cols[2].span.text == "W" or cols[2].span.text == "L":
                status = cols[2].span.text
            
            game_dict["result"] = status
            
            if cols[2].find("span", class_="ml4") != None:
                bscores = cols[2].find("span", class_="ml4").a.text.split("-")
                link = cols[2].find("span", class_="ml4").a['href']
                game_id = str(link.split('/')[7])

                game_dict['game_id'] = game_id
                # print("Game id - " + game_id)

                overtime = 0

                #if " OT" in bscores[1]:
                loc = bscores[1].find(" ")
                if loc > -1:
                    overtime = 1
                    bscores[1] = bscores[1][:loc]

                game_dict['overtime'] = str(overtime)

                if status == "W":
                    game_dict["score"] = str(bscores[0]).strip()
                    game_dict["opp_score"] = str(bscores[1]).strip()
                else:
                    game_dict["score"] = str(bscores[1]).strip()
                    game_dict["opp_score"] = str(bscores[0]).strip()

                get_game_matchup_data(team, season, game_id, game_dict)
            game_list.append(game_dict)
    
    # write to output file
    f = open(output_file_name, "w")
    writer = csv.writer(f)
    
    # get header (dictionary keys)
    sample_dict = game_list[0]
    writer.writerow(sample_dict.keys())

    for dictionary in game_list:
        writer.writerow(dictionary.values())
    f.close()

    print('step_2a_create_team_schedule_csv::done')