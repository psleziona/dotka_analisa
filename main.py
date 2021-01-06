import requests
from bs4 import BeautifulSoup
import json
import pprint

res = requests.get('https://api.opendota.com/api/proPlayers')
data = json.loads(res.text)

acc_id = list()
i=0
for player in data:
    acc_id.append(player.get('account_id', None))

hero_stats = dict()

for player in acc_id:
    total = 0
    hero_id = None
    looses = 0

    if i == 0:
        res = requests.get(f'https://api.opendota.com/api/players/{player}/heroes')
        jres = json.loads(res.text)
        # pprint.pprint(jres, indent=4)
        for heroes in jres[0]:
            looses = heroes['against_games'] - heroes['against_win']
            percent_loose = looses

    i += 1
        # hero = jres['hero_id']
        # hero_stats[hero] = hero_stats.get(hero, 0) + 1

print(hero_stats)
