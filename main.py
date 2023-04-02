from step_1_load_source_htmls import get_team_schedule_html
from step_2a_create_team_schedule_csv import generate_team_schedule_csv
from step_2b_create_game_boxscore_csv import generate_team_boxscore_csv

# Teams avilable
# "bos" : "Boston Celtics",
# "bkn" : "Brooklyn Nets",
# "ny" : "New York Knicks",
# "phi" : "Philadelphia 76ers",
# "tor" : "Toronto Raptors",

# "den" : "Denver Nuggets",
# "min" : "Minnesota Timberwolves",
# "okc" : "Oklahoma City Thunder",
# "por" : "Portland Trail Blazers",
# "utah" : "Utah Jazz",

# "chi" : "Chicago Bulls",
# "cle" : "Cleveland Cavaliers",
# "det" : "Detroit Pistons",
# "ind" : "Indiana Pacers",
# "mil" : "Milwaukee Bucks",

# "gs" : "Golden State Warriors",
# "lac" : "LA Clippers",
# "lal" : "Los Angeles Lakers",
# "phx" : "Phoenix Suns",
# "sac" : "Sacramento Kings",

# "atl" : "Atlanta Hawks",
# "cha" : "Charlotte Hornets",
# "mia" : "Miami Heat",
# "orl" : "Orlando Magic",
# "wsh" : "Washington Wizards",

# "dal" : "Dallas Mavericks",
# "hou" : "Houston Rockets",
# "mem" : "Memphis Grizzlies",
# "no" : "New Orleans Pelicans",
# "sa" : "San Antonio Spurs"

team = "bos"
season = 2023
get_team_schedule_html(team, season, True)
generate_team_schedule_csv(team, season)
generate_team_boxscore_csv(team, season)

