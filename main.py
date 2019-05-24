import json
import logging
from urllib import request

import feedparser

from anilist import fetch_user_list, fetch_watching
from anime_feed import search_title

logger = logging.getLogger('anime_downloader')
fh = logging.FileHandler('anime_downloader.log')
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
fh.setLevel(logging.INFO)
fh.setFormatter(formatter)
logger.setLevel(logging.INFO)
logger.addHandler(fh)

with open('settings.json') as f:
    settings = json.load(f)

if __name__ == '__main__':
    feed = feedparser.parse('https://nyaa.si/?page=rss')  # &magnets
    user_list = fetch_user_list(settings['Anilist']['username'], settings['Anilist']['token'])
    for item in fetch_watching(user_list):
        episode = item['progress'] + 1
        romaji_title = item['media']['title']['romaji']

        name_episode = f"{item['media']['title']['romaji']}-E{episode}"

        try:
            with open('downloaded.json'):
                pass
        except FileNotFoundError:
            with open('downloaded.json', 'w+'):
                pass

        with open('downloaded.json', 'r+') as f:
            try:
                downloaded = json.load(f)
            except json.decoder.JSONDecodeError:
                downloaded = {}

            downloaded_item = downloaded.get(romaji_title)

            if downloaded_item:
                if episode in downloaded_item.get('episodes'):
                    logger.info(f"[MAIN] Not downloading '{romaji_title}' E{episode}. Already marked as downloaded.")
                    continue

            link, name = search_title(feed, item['media']['title'], episode=episode)
            if link and name:
                request.urlretrieve(link, f'/home/john/Downloads/{romaji_title} E{episode}.torrent')
                logger.info(
                    f"[MAIN] Opening magnet link for anime "
                    f"'{name if name else item['media']['title']['romaji']}' E{episode}."
                )
                if downloaded_item:
                    downloaded[romaji_title]['episodes'].append(episode)
                    logger.info(f"[MAIN] Added E{episode} to '{romaji_title}'s download entry.")
                    json.dump(downloaded, f)
                else:
                    logger.info(f"[MAIN] Created download Entry for anime '{romaji_title}' starting with E{episode}.")
                    downloaded[romaji_title] = {'episodes': [episode]}
                    json.dump(downloaded, f)
            else:
                logger.info(f"[MAIN] No match found for anime '{name}' E{episode}.")

        with open('downloaded.json', 'w') as f:
            json.dump(downloaded, f)

    logger.info('\n')