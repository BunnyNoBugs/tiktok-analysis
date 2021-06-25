from TikTokApi import TikTokApi
import json


api = TikTokApi.get_instance()

count = 1800

query = 'ghosthoney'

tiktoks = api.by_username(query, count=count)

with open(f'data/user_{query}.json', 'w') as f:
    json.dump(tiktoks, f)
