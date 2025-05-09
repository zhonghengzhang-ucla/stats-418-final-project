import re
import time
from datetime import date

import pandas as pd
import requests
from bs4 import BeautifulSoup
from requests.exceptions import ConnectionError, ConnectTimeout
from unidecode import unidecode
from urllib3.exceptions import NameResolutionError, MaxRetryError

entries = []
df_player = pd.read_csv('outfield_players.csv')
df_gk = pd.read_csv('goalkeepers.csv')
outfield_players = []
goalkeepers = []
error_file = open('errors.txt', 'a')
default_url = 'https://fminside.net/players/3-fm-23/{}-{}'
headers = {'User-Agent': 'Requests by Zhongheng Zhang for schoolwork, please contact via zhonghengzhang@ucla.edu'}
with open('current_index.txt', 'r') as f:
    starting_point = int(f.read())

with open('alldata.csv', 'r', encoding='utf-8') as file:
    next(file)
    for line in file:
        if re.findall(r'\?', line):
            continue
        player_entry = re.sub(r'\n', '', line).split(',')
        player_entry[1] = re.sub(
            r'\s', '-', re.sub(r'[\'.]', '', unidecode(player_entry[1].lower())))
        entries.append(player_entry)

for i in range(starting_point, len(entries)):
    if i % 10 == 0:
        print(i)
        df_player = pd.concat([df_player, pd.DataFrame(outfield_players)]).drop_duplicates(subset='UID', keep='last')
        df_gk = pd.concat([df_gk, pd.DataFrame(goalkeepers)]).drop_duplicates(subset='UID', keep='last')
        df_player.to_csv('outfield_players.csv', index=False)
        df_gk.to_csv('goalkeepers.csv', index=False)
        with open('current_index.txt', 'w') as f:
            f.write(str(i))

    page_soup = BeautifulSoup(
        requests.get(
            default_url.format(entries[i][0], entries[i][1]), headers=headers).content,
        'lxml')
    print(default_url.format(entries[i][0], entries[i][1]))
    time.sleep(10)
    try:
        if 'dynamic' in page_soup.select_one('span#potential').attrs['class']:
            continue

        is_gk = False
        player_data = {'UID': entries[i][0]}
        for li in page_soup.select_one('div#player').select_one('div.column').select('li'):
            match li.select_one('span.key').text:
                case 'Position(s)':
                    player_data['Position(s)'] = li.select_one('span.desktop_positions').text
                    is_gk = 'GK' in player_data['Position(s)']
                case 'Height' | 'Weight':
                    player_data[
                        f'{li.select_one('span.key').text} ({li.select_one('span.value').text.split(' ')[-1]})'
                    ] = li.select_one('span.value').text.split(' ')[0]
                case 'Caps / Goals':
                    player_data['International Caps'] = li.select_one('span.value').text.split(' ')[0]
                    player_data['International Goals'] = li.select_one('span.value').text.split(' ')[-1]
                case _:
                    player_data[li.select_one('span.key').text] = li.select_one('span.value').text

        player_data['CA'] = page_soup.select_one('div#player span#ability').text
        player_data['PA'] = page_soup.select_one('div#player span#potential').text

        if page_soup.select_one('div#player').select('div.column')[1].select_one('h2').text == 'Contract':
            for li in page_soup.select_one('div#player').select('div.column')[1].select('li'):
                match li.select_one('span.key').text:
                    case 'Sell value' | 'Rel. clause':
                        match li.select_one('span.value').text:
                            case 'Not for sale':
                                player_data[f'{li.select_one('span.key').text} (€)'] = ''
                            case 'Free Transfer':
                                player_data[f'{li.select_one('span.key').text} (€)'] = 0
                            case _:
                                player_data[f'{li.select_one('span.key').text} (€)'] = \
                                    li.select_one('span.value').text.split(' ')[1].replace(',', '')
                    case 'Wages':
                        player_data['Wages (€)'] = li.select_one('span.value').text.split(' ')[1].replace(',', '')
                    case 'Contract end':
                        player_data['Contract expiration (year)'] = ((date.fromisoformat(
                            li.select_one('span.value').text) - date(2022, 7, 1)).days / 365).__round__(1)
                    case _:
                        player_data[li.select_one('span.key').text] = li.select_one('span.value').text
        else:
            player_data['Club'] = page_soup.select_one('div#player div.meta').select_one('span.value').text

        for attribute_column in page_soup.select_one('div#right_column div#player_stats').select('table'):
            for tr in attribute_column.select('tr'):
                player_data[tr.select_one('acronym').text] = int((int(tr.select_one('td.stat').text) / 5).__round__(0))

        if is_gk:
            goalkeepers.append(player_data)
        else:
            outfield_players.append(player_data)

    except (AttributeError, ValueError) as e:
        print(e)
        print(entries[i][0], 'dropped')
        error_file.writelines(default_url.format(entries[i][0], entries[i][1]) + '\n')
        error_file.flush()
        continue

    except (ConnectionError, NameResolutionError, MaxRetryError, ConnectTimeout) as e:
        print(e)
        print('Abort at', entries[i][0])
        with open('current_index.txt', 'w') as f:
            f.write(str(i))
        break

df_player = pd.concat([df_player, pd.DataFrame(outfield_players)]).drop_duplicates(subset='UID', keep='last')
df_gk = pd.concat([df_gk, pd.DataFrame(goalkeepers)]).drop_duplicates(subset='UID', keep='last')
df_player.to_csv('outfield_players.csv', index=False)
df_gk.to_csv('goalkeepers.csv', index=False)
error_file.close()
