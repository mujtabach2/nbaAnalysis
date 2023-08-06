import pandas as pd 
import streamlit as st
import plotly.express as px
from data import get_player_career_stats
import numpy as np
from functions import opponent_analysis
from functions import analysis
df = pd.read_csv('NBALineup2021.csv')

# Title for app
st.set_page_config(layout="wide")
st.title('NBA Lineup Analysis Tool ')

# User chooses team 
team1 = st.selectbox(
    'Choose Team:',
    df['team'].unique())



# Get the selected teams
df_team1 = df[df['team'] == team1].reset_index(drop=True)
srt = ['PTS_RANK', 'FGM_RANK', 'FGA_RANK', 'FG_PCT_RANK', 'FG3M_RANK', 'FG3A_RANK', 'FG3_PCT_RANK', 'FTM_RANK', 'FTA_RANK', 'FT_PCT_RANK', 'OREB_RANK', 'DREB_RANK', 'REB_RANK', 'AST_RANK', 'TOV_RANK', 'STL_RANK', 'BLK_RANK', 'BLKA_RANK', 'PF_RANK', 'PFD_RANK', 'PLUS_MINUS_RANK', 'NBA_FANTASY_PTS_RANK', 'DD2_RANK', 'TD3_RANK', 'CFID', 'CFPARAMS']
sort_value = st.selectbox(
    'Choose Sort Value:',
    srt)
    
df_team1 = df_team1.sort_values(by=sort_value)

# Get players on roster for each team
df_team1['players_list'] = df_team1['players_list'].str.replace(r"[\"\' \[\]]", '')
duplicate_roster1 = df_team1['players_list'].apply(pd.Series).stack()
roster1 = duplicate_roster1.unique()


# Let the user select the names of the premade roster
roster1_selected = st.selectbox(
    f'Select players from {team1}:',
    roster1)
    # roster1_selected.append(name)

#roster1_selected=roster1_selected.split(', ')

df_lineup1 = df_team1[df_team1['players_list'].apply(lambda x: set(x) == set(roster1_selected))]


roster1_cleaned = [name.strip("[]' ") for name in df_team1['players_list'].str.split(',')[0]]
player_id_mapping = {}
for index, row in df.iterrows():
    players_list = row['players_list']
    player_names = [name.strip() for name in players_list[2:-2].split("', '")]  # Split player names
    player_ids = row['GROUP_ID'][1:-1].split('-')  # Split player IDs
    for i, player_name in enumerate(player_names):
        player_id = player_ids[i]
        player_id_mapping[player_name] = player_id

# ... (rest of your code)

# Clean up roster1 and roster2


player_ids1 = {}


# Get player IDs for selected players and store in dictionaries
for player_name in roster1_cleaned:
    if player_name in player_id_mapping:
        player_ids1[player_name] = player_id_mapping[player_name]




analysis(df_lineup1, df_team1, team1, roster1_selected, player_ids1, df, sort_value)
 
