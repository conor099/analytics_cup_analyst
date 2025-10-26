#%% Imports.
import requests
import pandas as pd
import json
import numpy as np
from kloppy import skillcorner

#%% Extract data for one match.

all_open_match_ids = [1886347, 1899585, 1925299, 1953632, 1996435, 2006229, 2011166, 2013725, 2015213, 2017461]
match_id = all_open_match_ids[0]

#%% Define function to clean a match's tracking data.

def load_tracking_dataframes(match_id):
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

#%% Testing load of events data.

events_url = f"https://raw.githubusercontent.com/SkillCorner/opendata/master/data/matches/{match_id}/{match_id}_dynamic_events.csv"
events_data = pd.read_csv(events_url)

#%% Testing load of phases of play data.

pop_url = f"https://raw.githubusercontent.com/SkillCorner/opendata/master/data/matches/{match_id}/{match_id}_phases_of_play.csv"
pop_data = pd.read_csv(pop_url)