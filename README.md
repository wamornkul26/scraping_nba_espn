# scraping_nba_espn

## Prerequisites: 
- python 
- Beautiful Soup

## Background:
I developed an app for analyzing data related to the Golden State Warriors and needed to gather data for my project. As part of the project, I wanted to do web scraping using Beautiful Soup. I chose to scrape data from the ESPN website because I have been a regular visitor for years. While other websites offer NBA stats in simpler, tabular formats, I deliberately selected ESPN's more complex format to challenge myself and facilitate learning.

## Target Pages 
The pages that I'm scraping are as followed:

1. https://www.espn.com/nba/team/schedule/_/name/[team code]/[team name]
    - This page contains the team schedules for the whole season. Each game contains the "game_id" field which is required to pull data for the other two URLs.

2. https://www.espn.com/nba/matchup/_/gameId/[game_id]
    - This page contains the Team Stats for that given game.

3. https://www.espn.com/nba/boxscore/_/gameId/[game_id]
    - This page contains players data for that given game.


## Scraping Action
My codes are divided into four files:
1. main.py - This is the main file to run/modify to retrieve data for the selected team and season.
2. step_1_load_source_htmls.py - This script will retrieve the necessary web pages and store them under ./inpus/html/[team_name]/[season]/ directory.  You should expect to see 1 Team Schedule html file, 82 (assuming the season is completd) matchup files and 82 boxscore files.  I tried to be courteous about this, so if the file has already been downloaded, then the code won't send a request to the ESPN website again.
3. step_2a_create_team_schedule_csv.py - This file scrapes data and combines the Team schedule page and 82 matchup files into one single csv file. The result will be store in the ./outputs/csv/[team_name]/[season]/ directory.
4. step_2b_create game_boxscore_csv.py - This script extracts data from the 82 boxscore files and combine them into a single csv file. The csv file will be store in the ./outputs/csv/[team_name]/[season]/ directory.

