from TikTokApi import TikTokApi
import json


api = TikTokApi.get_instance()

count = 1800

tiktoks = api.by_hashtag('popit', count=count)

with open('data/#popit.json', 'w') as f:
    json.dump(tiktoks, f)
