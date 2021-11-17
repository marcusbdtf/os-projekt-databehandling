import pandas as pd
import hashlib as hl
"""Data"""
athletes = pd.read_csv("Data/athlete_events.csv")
hashed_names = athletes["Name"].apply(lambda x: hl.sha256(x.encode()).hexdigest())
athletes.insert(1,"Hashed name", hashed_names)
athletes = athletes.drop(columns="Name")
athletes["Total"] = athletes["ID"]
athletes = athletes.drop_duplicates(subset=["Medal", "Games","Event"])
athletes.drop(axis=1, columns=["ID", "Hashed name", "Team"], inplace=True)

all_countries_df = athletes.reset_index()
italy_df = athletes[athletes["NOC"]=="ITA"].drop(axis=1, columns="NOC").reset_index()

def get_italy_data():
    return italy_df

def get_all_countries():
    return all_countries_df

def process_data(old_df, col):
    filtered_df = old_df.groupby(col).count().reset_index()
    filtered_df = filtered_df.sort_values(by="Total", ascending=False)
    filtered_df = filtered_df[filtered_df[col].notna()]

    return filtered_df