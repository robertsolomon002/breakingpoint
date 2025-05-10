import re
from selenium import webdriver
from selenium.webdriver.common.by import By
import pandas as pd
import time
import requests
from bs4 import BeautifulSoup

import sys
sys.stdout.reconfigure(encoding='utf-8')



            

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


    
    
    #print(maps)
    #print(maps[0].split())
    #print(rows)
#analyzing_game("https://www.breakingpoint.gg/match/93863/Vegas-Falcons-vs-LA-Guerrillas-M8-at-CDL-Major-1-Qualifier-2025")
#analyzing_game("https://www.breakingpoint.gg/match/94004/Los-Angeles-Thieves-vs-Vancouver-Surge-at-CDL-Major-3-Tournament-2025")
analyzing_game("https://www.breakingpoint.gg/match/93885/Atlanta-FaZe-vs-Los-Angeles-Thieves-at-CDL-Major-1-Tournament-2025")