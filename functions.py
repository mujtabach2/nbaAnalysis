import streamlit as st
import pandas as pd
import plotly.express as px
from data import get_player_career_stats


def opponent_analysis(team1, team2, compare_value):
    """
    Compares the two teams' ppg, fg, 3p%, tov, stl, blk, eFG, ts%, AST/TO.

    Args:
        team1 (str): The name of the first team.
        team2 (str): The name of the second team.

    Returns:
        None.
    """
    df = pd.read_csv('NBALineup2021.csv')
    
    df_team1 = df[df['team'] == team1].reset_index(drop=True)
    df_team2 = df[df['team'] == team2].reset_index(drop=True)
    df_team2 = df_team2.sort_values(by=compare_value,ascending=False)
    
    # Get the data for the two teams
    df_team1['ppg'] = df_team1['PTS'] / df_team1['GP']
    df_team1['fg'] = (df_team1['FGM'] + 0.5 * df_team1['FG3M']) / df_team1['FGA']
    df_team1['3p%'] = df_team1['FG3M'] / df_team1['FG3A']
    df_team1['tov'] = df_team1['TOV'] / df_team1['GP']
    df_team1['stl'] = df_team1['STL'] / df_team1['GP']
    df_team1['blk'] = df_team1['BLK'] / df_team1['GP']
    df_team1['eFG%'] = (df_team1['FGM'] + 0.5 * df_team1['FG3M']) / df_team1['FGA']
    df_team1['ts%'] = (df_team1['PTS'] / (2 * (df_team1['FGA'] + 0.44 * df_team1['FTA']))) * 100
    df_team1['AST/TO'] = df_team1['AST'] / df_team1['TOV']

    df_team2['ppg'] = df_team2['PTS'] / df_team2['GP']
    df_team2['fg'] = (df_team2['FGM'] + 0.5 * df_team2['FG3M']) / df_team2['FGA']
    df_team2['3p%'] = df_team2['FG3M'] / df_team2['FG3A']
    df_team2['tov'] = df_team2['TOV'] / df_team2['GP']
    df_team2['stl'] = df_team2['STL'] / df_team2['GP']
    df_team2['blk'] = df_team2['BLK'] / df_team2['GP']
    df_team2['eFG%'] = (df_team2['FGM'] + 0.5 * df_team2['FG3M']) / df_team2['FGA']
    df_team2['ts%'] = (df_team2['PTS'] / (2 * (df_team2['FGA'] + 0.44 * df_team2['FTA']))) * 100
    df_team2['AST/TO'] = df_team2['AST'] / df_team2['TOV']

    col1,col2 = st.columns(2)
    sdas = df_team2['players_list'].values[0].replace('[', '').replace(']', '').replace(",", ' - ').replace("'", '')
    
    with col1:
        st.write(f"## {team1}")
        st.dataframe(df_team1[['ppg', 'fg', '3p%', 'tov', 'stl', 'blk', 'eFG%', 'ts%', 'AST/TO']])
    with col2:
        st.write(f"## {team2}")
        st.dataframe( df_team2[['ppg', 'fg', '3p%', 'tov', 'stl', 'blk', 'eFG%', 'ts%', 'AST/TO']])
        st.write(f'Lineup: {sdas}')
                            
 


    


                        
def analysis(df_lineup1, df_team1, team1, players1, player_ids1, df, sort_value):

    st.write(f"## Lineup for {team1}")
    cola, colb = st.columns(2)
    with cola:
        st.write("### Team Stats")
        columns_to_divide = ['PTS', 'AST', 'REB', 'STL', 'BLK']
        divisor = df_lineup1['GP']
        if divisor.values[0] != 0:
            df_lineup1[columns_to_divide] = df_lineup1[columns_to_divide] / divisor.values[0]

        df_important = df_lineup1[['MIN', 'PLUS_MINUS', 'FG_PCT', 'FG3_PCT', 'PTS', 'AST', 'REB', 'STL', 'BLK', sort_value]]
        st.dataframe(df_important)
    with colb:
        st.write("### Efficiency Metrics Comparison")
        efg = (df_lineup1['FGM'] + 0.5 * df_lineup1['FG3M']) / df_lineup1['FGA']
        ts = df_lineup1['PTS'] / (2 * (df_lineup1['FGA'] + 0.44 * df_lineup1['FTA']))
        df_efficiency = pd.DataFrame({'eFG%': [efg.values[0]], 'TS%': [ts.values[0]]})
        st.dataframe(df_efficiency)

    st.write('## Team Analysis')
    col1, col2, col3, col4, col5, col6, col7, col8, col9 = st.columns(9)



    # Display the team's cumulative stats in columns
    col1, col2, col3, col4, col5, col6, col7, col8, col9 = st.columns(9)
    with col1:
        fig_min = px.histogram(df_team1, x="MIN", title="Minutes")
        fig_min.add_vline(x=pd.Series(df_important['MIN']).values[0], line_color='red')
        st.plotly_chart(fig_min, use_container_width=True)

    with col2:
        fig_pm = px.histogram(df_team1, x="PLUS_MINUS", title="Plus Minus")
        fig_pm.add_vline(x=pd.Series(df_important['PLUS_MINUS']).values[0], line_color='red')
        st.plotly_chart(fig_pm, use_container_width=True)

    with col3:
        fig_fg = px.histogram(df_team1, x="FG_PCT", title="Field Goal %")
        fig_fg.add_vline(x=pd.Series(df_important['FG_PCT']).values[0], line_color='red')
        st.plotly_chart(fig_fg, use_container_width=True)

    with col4:
        fig_3p = px.histogram(df_team1, x="FG3_PCT", title="3-Point %")
        fig_3p.add_vline(x=pd.Series(df_important['FG3_PCT']).values[0], line_color='red')
        st.plotly_chart(fig_3p, use_container_width=True)

    with col5:
        fig_pts = px.histogram(df_team1, x="PTS", title="Points per game")
        fig_pts.add_vline(x=pd.Series(df_important['PTS']).values[0], line_color='red')
        st.plotly_chart(fig_pts, use_container_width=True)

    with col6:
        fig_ast = px.histogram(df_team1, x="AST", title="Assists per game")
        fig_ast.add_vline(x=pd.Series(df_important['AST']).values[0], line_color='red')
        st.plotly_chart(fig_ast, use_container_width=True)

    with col7:
        fig_reb = px.histogram(df_team1, x="REB", title="Rebounds per game")
        fig_reb.add_vline(x=pd.Series(df_important['REB']).values[0], line_color='red')
        st.plotly_chart(fig_reb, use_container_width=True)

    with col8:
        fig_stl = px.histogram(df_team1, x="STL", title="Steals per game")
        fig_stl.add_vline(x=pd.Series(df_important['STL']).values[0], line_color='red')
        st.plotly_chart(fig_stl, use_container_width=True)

    with col9:
        fig_blk = px.histogram(df_team1, x="BLK", title="Blocks per game")
        fig_blk.add_vline(x=pd.Series(df_important['BLK']).values[0], line_color='red')
        st.plotly_chart(fig_blk, use_container_width=True)
   
    st.write("## Advanced Stats")
    # Advanced Stats
    selected_player1 = st.selectbox(
        'Select a player from Team 1:',
        player_ids1.keys())

    # Retrieve career stats for the selected player
    selected_player_id1 = player_ids1.get(selected_player1)
    if selected_player_id1:
        try:
            col1, col2 = st.columns(2)
            selected_player_stats = get_player_career_stats(selected_player_id1)
            # Drop the 'PLAYER_ID' column before displaying the DataFrame
            selected_player_stats = selected_player_stats.drop(columns=['PLAYER_ID', 'LEAGUE_ID', 'TEAM_ID'])
            with col1:
                st.write(f"### Career Stats for {selected_player1}")
                st.dataframe(selected_player_stats)
            
            
                    # Calculate Player Efficiency Rating (PER)
            selected_player_stats['PER'] = (
                (selected_player_stats['PTS'] + selected_player_stats['AST'] + selected_player_stats['REB']
                + selected_player_stats['STL'] + selected_player_stats['BLK'])
                - (selected_player_stats['FGA'] - selected_player_stats['FGM']) - (selected_player_stats['FTA'] - selected_player_stats['FTM'])
                - selected_player_stats['TOV']) / selected_player_stats['GP']

            # Calculate True Shooting Percentage (TS%)
            selected_player_stats['TS%'] = (
                selected_player_stats['PTS'] / (2 * (selected_player_stats['FGA'] + 0.44 * selected_player_stats['FTA']))) * 100

            # Calculate Effective Field Goal Percentage (eFG%)
            selected_player_stats['eFG%'] = (
                (selected_player_stats['FGM'] + 0.5 * selected_player_stats['FG3M'])
                / selected_player_stats['FGA'])

            # Calculate Assist-to-Turnover Ratio (AST/TO)
            selected_player_stats['AST/TO'] = (
                selected_player_stats['AST'] / selected_player_stats['TOV'])

            # Calculate Rebound Rate (RR)
            selected_player_stats['RR'] = (
                selected_player_stats['REB'] / selected_player_stats['MIN']) * 48
            
            average_advanced_metrics = selected_player_stats[['PER', 'TS%', 'eFG%', 'AST/TO', 'RR']].mean()

        # Display the calculated average of advanced metrics
            with col2:
                st.write(f"### Average of Advanced Metrics for {selected_player1} (Career)")
                st.dataframe(average_advanced_metrics)
        except Exception as e:
            st.write(f"Error retrieving career stats for player {selected_player1}: {str(e)}")
    else:
        st.write("Selected player not found in the player IDs.")

    # Opponent Analysis
    st.write("### Opponent Analysis")
    
    team2 = st.selectbox(
    '# Choose Team to compare:',
    df['team'].unique())
    compare_value = st.selectbox(
        '# Choose Stat to prioritize:',
        ['PTS', 'FGM', 'FGA', 'FG_PCT', 'FG3M', 'FG3A', 'FG3_PCT', 'FTM', 'FTA', 'FT_PCT', 'OREB', 'DREB', 'REB', 'AST', 'TOV', 'STL', 'BLK', 'BLKA', 'PF', 'PFD', 'PLUS_MINUS', 'NBA_FANTASY_PTS', 'DD2', 'TD3', 'CFID', 'CFPARAMS'])
        
    opponent_analysis(team1, team2, compare_value)
