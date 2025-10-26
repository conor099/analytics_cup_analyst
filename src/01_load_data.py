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

    return tracking_df


clean_tracking_data = load_tracking_dataframes(match_id=match_id)