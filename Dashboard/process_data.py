import pandas as pd
import hashlib as hl
"""Data"""
athletes = pd.read_csv("Data/athlete_events.csv")
hashed_names = athletes["Name"].apply(lambda x: hl.sha256(x.encode()).hexdigest())
athletes.insert(1,"Hashed name", hashed_names)
athletes = athletes.drop(columns="Name")
italy_df = athletes.drop_duplicates(subset=["Medal", "Games","Event"])
italy_df = italy_df[italy_df["NOC"]=="ITA"]
italy_df["Total"] = italy_df["ID"]

def get_italy_data():
    return italy_df.drop(axis=1,columns=["ID", "Hashed name", "Team", "NOC"])

def process_data(old_df, col):
    filtered_df = old_df.groupby(col).count().reset_index()
    filtered_df = filtered_df.sort_values(by="Total", ascending=False)
    return filtered_df