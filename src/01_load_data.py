#%% Imports.
import requests
import pandas as pd
import json
import numpy as np
from kloppy import skillcorner
import matplotlib.pyplot as plt

#%% Extract data for one match.

all_open_match_ids = [1886347, 1899585, 1925299, 1953632, 1996435, 2006229, 2011166, 2013725, 2015213, 2017461]
match_id = all_open_match_ids[0]

#%% Define function to clean a match's tracking data.

def load_tracking_dataframes(match_id : int):
    """
    :param      match_id:       SkillCorner match id.
    :return[0]: tracking_df:    Cleaned tracking data for selected match id.
    :return[1]: match_metadata: Metadata for selected match id.
    """
    # Load tracking data for specific match id.
    match_tracking_data = skillcorner.load_open_data(match_id=match_id)

    # Extract metadata for match.
    match_metadata = match_tracking_data.metadata

    # Convert tracking data to dataframe. NB: Don't do this step before extracting metadata, gives an error.
    match_tracking_data = match_tracking_data.to_df()

    # Drop any columns from the tracking data if all values are NaN/None.
    tracking_df = match_tracking_data.dropna(axis=1, how="all")

    # Seems like all frames included are only when ball is in play. Drop ball_state column if all values = 'alive'.
    if (tracking_df["ball_state"] == "alive").all():
        tracking_df = tracking_df.drop(columns=["ball_state"])

    return tracking_df, match_metadata


clean_tracking_data, metadata = load_tracking_dataframes(match_id=match_id)

#%% Function to visualise the tracking data.

def visualise_tracking_data(tracking_data : pd.DataFrame):

    # Find the x and y column names for each player. All player coordinate columns start with a number.
    player_cols = [col for col in tracking_data.columns if col[0].isdigit()]

    # Extract all player ids from column names.
    player_ids = set([int(player_id.split("_")[0]) for player_id in player_cols])

    first_frame = tracking_data.iloc[20000]

    # Collect player positions
    player_positions = []
    for pid in player_ids:
        x_col, y_col = f"{pid}_x", f"{pid}_y"
        if x_col in tracking_data.columns and y_col in tracking_data.columns:
            x, y = first_frame[x_col], first_frame[y_col]
            player_positions.append((pid, x, y))

    # Ball position (find dynamically in case column order differs)
    ball_x = first_frame.filter(regex='ball_x').iloc[0]
    ball_y = first_frame.filter(regex='ball_y').iloc[0]

    # Plot setup
    plt.figure(figsize=(10, 7))
    plt.scatter(
        [x for _, x, _ in player_positions],
        [y for _, _, y in player_positions],
        color='blue', label='Players'
    )
    plt.scatter(ball_x, ball_y, color='red', marker='*', s=200, label='Ball')

    # Annotate players
    for pid, x, y in player_positions:
        if pd.notna(x) and pd.notna(y):
            plt.text(x, y + 0.005, pid, fontsize=8, ha='center', color='black')

    # Style the field
    plt.xlim(0, 1)
    plt.ylim(0, 1)
    plt.gca().set_aspect('equal', adjustable='box')
    plt.xlabel("X Position")
    plt.ylabel("Y Position")
    plt.title("Players and Ball - First Frame")
    plt.legend()
    plt.grid(alpha=0.3)
    plt.show()

visualise_tracking_data(tracking_data=clean_tracking_data)

#%%
print(metadata.teams)

#%% Testing load of events data.

events_url = f"https://raw.githubusercontent.com/SkillCorner/opendata/master/data/matches/{match_id}/{match_id}_dynamic_events.csv"
events_data = pd.read_csv(events_url)

#%% Testing load of phases of play data.

pop_url = f"https://raw.githubusercontent.com/SkillCorner/opendata/master/data/matches/{match_id}/{match_id}_phases_of_play.csv"
pop_data = pd.read_csv(pop_url)