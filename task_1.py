import requests
import json


def find_intelligence_superhero():
    heroes_list = get_all_heroes()

    hulk_data = find_hero_by_name(heroes_list, 'Hulk')
    ca_data = find_hero_by_name(heroes_list, 'Captain America')
    thanos_data = find_hero_by_name(heroes_list, 'Thanos')

    current_id = hulk_data['id']
    max_intelligence = hulk_data['powerstats']['intelligence']

    for hero in [ca_data, thanos_data]:
        if max_intelligence < hero['powerstats']['intelligence']:
            max_intelligence = hero['powerstats']['intelligence']
            current_id = hero['id']

    return current_id

def find_hero_by_name(heroes, name):
    return [hero for hero in heroes if hero['name'] == name][0]

def get_all_heroes():
    res = requests.get('https://akabab.github.io/superhero-api/api/all.json')
    return json.loads(res.text)