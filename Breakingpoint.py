import re
from selenium import webdriver
from selenium.webdriver.common.by import By
import pandas as pd
import time
import requests
from bs4 import BeautifulSoup
import os
import csv
import shutil
import tkinter as tk

import sys
sys.stdout.reconfigure(encoding='utf-8')


team_properties = ['team_id','name']
event_properties = ['event_id','name','year','is_lan','is_bracket']
            

def analyzing_game(url):
    resp = requests.get(url)
    resp.raise_for_status()

    soup = BeautifulSoup(resp.text, 'lxml')
    #print(soup)
    title = soup.title.string.split(' - ', 1)[0]
    vs = title.split(' vs ')
    at = vs[1].split(' at ')
    left_team = vs[0]
    right_team = at[0]
    event = at[1]
  
    print(title)
    print(left_team)
    print(right_team)
    print(event)
    maps = soup.find_all(string=re.compile(r"^Map\s*.:"))
    rows = soup.find_all('tr', class_='css-e5a2k5')
    total_maps = len(maps)
    map_order = ['hp', 'snd','ctl']
    map_counter = 0
    player_counter = 0
    
    html = str(soup)
    m = re.search(
        r'"round"\s*:\s*{\s*[^}]*"name"\s*:\s*"([^"]+)"',
        html
    )
    if m:
        print(m.group(1))
    else:
        print("No")
    for row in rows:

        # grab all cells, strip whitespace & commas
        cells = [td.get_text(strip=True).replace(',', '') 
                 for td in row.find_all('td')]
        if len(cells) >= 3:
            if player_counter == 0:
                map_info = maps[map_counter].split(' - ')[0]
                map_split = map_info.split(': ')
                map_number = map_split[0].split(' ')[1]
                map_name = map_split[1].split(' ')[0]
                
                if map_counter ==6:
                    map_mode = map_order[1]
                else:
                    map_mode = map_order[map_counter % 3]
                
                
                print(map_info)
                print(map_number)
                print(map_name)
                print(map_mode)
            #name, stat1, stat2 = cells[0], cells[1], cells[2]
            #print(f"{name}: {stat1}, {stat2}")
            print(cells)
            player_counter += 1
            if player_counter == 8:
                player_counter = 0
                map_counter += 1



def fetch_matches_json():
    url = "https://www.breakingpoint.gg/_next/data/9Lfvb0gTVgKdo31e4Oy_h/matches.json"
    resp = requests.get(url)
    resp.raise_for_status()          # make sure we got a 200 OK
    data = resp.json()               # parse the JSON into Python dict/list
    #data
    return data['pageProps']['allMatches']

def fetch_teams_json():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    csv_path = os.path.join(script_dir, 'teams.csv')
    fobj = open(csv_path, "w", newline='', encoding='utf-8')

    #print(team_properties)
    writer = csv.writer(fobj)

        
    writer.writerow(team_properties)
    url = "https://www.breakingpoint.gg/_next/data/9Lfvb0gTVgKdo31e4Oy_h/matches.json"
    resp = requests.get(url)
    resp.raise_for_status()          # make sure we got a 200 OK
    data = resp.json()               # parse the JSON into Python dict/list
    all_teams = data['pageProps']['allTeams']
        #return data['pageProps']['allTeams']
    for i in range(0,12):
        writer.writerow([all_teams[i]['id'], all_teams[i]['name']])
    
    fobj.close()

    print(data['pageProps'].keys())

def fetch_events_json():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    csv_path = os.path.join(script_dir, 'events.csv')
    fobj = open(csv_path, "w", newline='', encoding='utf-8')

    #print(team_properties)
    writer = csv.writer(fobj)

        
    writer.writerow(event_properties)
    url = "https://www.breakingpoint.gg/_next/data/9Lfvb0gTVgKdo31e4Oy_h/matches.json"
    resp = requests.get(url)
    resp.raise_for_status()          # make sure we got a 200 OK
    data = resp.json()               # parse the JSON into Python dict/list
    all_events = data['pageProps']['allEvents']
        #return data['pageProps']['allTeams']
    for i in range(0,len(all_events)):
        event = all_events[i]
        if (event["season_id"] == 2025 and event["division_id"] == 3 ):
            bracket = False
            if (event["tier"] == "Tournament"):
                bracket = True
            lan = False
            if (event["type"] == "Offline"):
                lan = True
            
            print(event["name"] + str(bracket) +str(lan))
            writer.writerow([event["id"], event["name"],event["season_id"],lan, bracket])
    
    fobj.close()

    #print(maps)
    #print(maps[0].split())
    #print(rows)
#analyzing_game("https://www.breakingpoint.gg/match/93863/Vegas-Falcons-vs-LA-Guerrillas-M8-at-CDL-Major-1-Qualifier-2025")
#analyzing_game("https://www.breakingpoint.gg/match/94004/Los-Angeles-Thieves-vs-Vancouver-Surge-at-CDL-Major-3-Tournament-2025")
#analyzing_game("https://www.breakingpoint.gg/match/93885/Atlanta-FaZe-vs-Los-Angeles-Thieves-at-CDL-Major-1-Tournament-2025")
#analyzing_game("https://www.breakingpoint.gg/match/94036/Miami-Heretics-vs-Minnesota-R%C3%98KKR-at-CDL-Major-4-Tournament-2025")



#fetch_teams_json()

#fetch_events_json()
#print(len(all_teams))


#for i in range(93815, 94053):
#    print(i)
#    string ="https://www.breakingpoint.gg/match/"
#    link = string + str(i)
#    analyzing_game(link)

def fetch_player_stats():
    url = (
        "https://dfpiiufxcciujugzjvgx.supabase.co/rest/v1/player_stats"
    )
    params = {
        # select all columns, filter game_id in the given list
        "select": "*",
        "game_id": "in.(0e002cdd-e542-410a-99da-9a1c0a7be92f,c76b2c19-20fd-48d4-892d-4f1a39b97071,083da935-3869-441a-8587-13942b6d3ee3,e3b54f3d-59cc-4206-ab17-69b4740bc7eb,20efb917-2521-438b-948e-18f65df0222d,a74cde01-ece5-434c-b691-1534ffbe8389)"
    }
    headers = {
        "apikey": (
            "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImRmcGlpdWZ4Y2NpdWp1Z3pqdmd4Iiwicm9sZSI6ImFub24iLCJpYXQiOjE3NDQ2ODk0MDMsImV4cCI6MjA2MDI2NTQwM30.36VuOTvrxtmR3nb-u3nnVYWzMBn9YP1bQFvUYF5T1OE"
        )
        #"Authorization": (
        #    "Bearer eyJhbGciOiJIUzI1NiIsImtpZCI6IkU4dnl4RXNCU1hxNFlIYzAiLCJ0eXAiOiJKV1QifQ.eyJpc3MiOiJodHRwczovL2RmcGlpdWZ4Y2NpdWp1Z3pqdmd4LnN1cGFiYXNlLmNvL2F1dGgvdjEiLCJzdWIiOiI5ZDc4MWNhYi0zMjk2LTRhOWQtOWJiZi02MzkwM2NkNGZlM2EiLCJhdWQiOiJhdXRoZW50aWNhdGVkIiwiZXhwIjoxNzQ4NTcwMzk2LCJpYXQiOjE3NDg1NjY3OTYsImVtYWlsIjoiMGdqdWFuY2VuYUBnbWFpbC5jb20iLCJwaG9uZSI6IiIsImFwcF9tZXRhZGF0YSI6eyJwcm92aWRlciI6Imdvb2dsZSIsInByb3ZpZGVycyI6WyJnb29nbGUiXSwic2VlX29ubHlfY2RsIjoidHJ1ZSIsInRoZW1lX3ByZWZlcmVuY2UiOiJkYXJrIn0sInVzZXJfbWV0YWRhdGEiOnsiYXZhdGFyX3VybCI6Imh0dHBzOi8vbGgzLmdvb2dsZXVzZXJjb250ZW50LmNvbS9hL0FDZzhvY0xpZ0xDMi0zNGEzcWdqQ3NtTUluS3FPWjI2ZWhGRUFBQ3hpWkRZMElKSWluRGxSN1E1PXM5Ni1jIiwiYnBfdXNlcl9pZCI6OTA2MiwiYnBfdXNlcm5hbWUiOiJicC1mZDQ3MDAyNSIsImVtYWlsIjoiMGdqdWFuY2VuYUBnbWFpbC5jb20iLCJlbWFpbF92ZXJpZmllZCI6dHJ1ZSwiZnVsbF9uYW1lIjoiSnVhbiBDZW5hIiwiaXNzIjoiaHR0cHM6Ly9hY2NvdW50cy5nb29nbGUuY29tIiwibmFtZSI6Ikp1YW4gQ2VuYSIsInBob25lX3ZlcmlmaWVkIjpmYWxzZSwicGljdHVyZSI6Imh0dHBzOi8vbGgzLmdvb2dsZXVzZXJjb250ZW50LmNvbS9hL0FDZzhvY0xpZ0xDMi0zNGEzcWdqQ3NtTUluS3FPWjI2ZWhGRUFBQ3hpWkRZMElKSWluRGxSN1E1PXM5Ni1jIiwicHJvdmlkZXJfaWQiOiIxMTU2NTU2MDcwMDEyOTU0NzEyNjQiLCJzdWIiOiIxMTU2NTU2MDcwMDEyOTU0NzEyNjQifSwicm9sZSI6ImF1dGhlbnRpY2F0ZWQiLCJhYWwiOiJhYWwxIiwiYW1yIjpbeyJtZXRob2QiOiJwYXNzd29yZCIsInRpbWVzdGFtcCI6MTc0NjQxNjkwOX1dLCJzZXNzaW9uX2lkIjoiMGE4YjdkMzUtMmU5MS00YTJiLTlkMmEtYmQ5OWMzMDVkNGIxIiwiaXNfYW5vbnltb3VzIjpmYWxzZX0.SOsnrlHrL2vNb6MMszllzgmUZvfE_76Z1dtCqAa82Ps"
        #)
    }

    r = requests.get(url, headers=headers, params=params)
    r.raise_for_status()
    print(r.json())


#fetch_player_stats()