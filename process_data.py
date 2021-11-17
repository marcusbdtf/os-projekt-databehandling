import pandas as pd
import hashlib as hl
"""Data"""
athletes = pd.read_csv("Data/athlete_events.csv")
hashed_names = athletes["Name"].apply(lambda x: hl.sha256(x.encode()).hexdigest())
athletes.insert(1,"Hashed name", hashed_names)
athletes = athletes.drop(columns="Name")
athletes["Total"] = athletes["ID"]
athletes = athletes.drop_duplicates(subset=["Medal", "Games","Event"])
athletes.drop(axis=1, columns=["ID", "Hashed name", "Team", "Event", "City", "Games", "Year", "Season", "Sex"], inplace=True)

all_countries_df = athletes.reset_index()

sp1 = pd.read_csv("Data/athlete_events.csv")
hashed_names = sp1["Name"].apply(lambda x: hl.sha256(x.encode()).hexdigest())
sp1.insert(1,"Hashed name", hashed_names)
sp1 = sp1.drop(columns="Name")
sp1 = sp1.drop_duplicates(subset=["Medal", "Games","Event"])
sp1.drop(axis=1, columns=["ID", "Hashed name", "Team", "Event", "City", "Games", 'Year', 'Season'], inplace=True)
sp2 = sp1.reset_index()

sports_df = sp2[all_countries_df['Sport'].isin(['Football', 'Basketball', 'Bobsleigh', 'Weightlifting'])]

italy_df = athletes[athletes["NOC"]=="ITA"].drop(axis=1, columns="NOC").reset_index()



def get_italy_data():
    return italy_df

def get_all_countries():
    return all_countries_df

def get_all_sports():
    return sports_df

def process_data(old_df, col):
    filtered_df = old_df.groupby(col).count().reset_index()
    filtered_df = filtered_df.sort_values(by="Total", ascending=False)
    filtered_df = filtered_df[filtered_df[col].notna()]
    return filtered_df

def process_countries(old_df, col):
    filtered_df = old_df.groupby('NOC').count().reset_index()
    filtered_df = filtered_df.sort_values(by='Medal', ascending=False)[:10]
    filtered_df = filtered_df[filtered_df[col].notna()]
    return filtered_df