from guessit import guessit
from fuzzywuzzy import fuzz

import logging

logger = logging.getLogger('anime_downloader')


def search_title(feed, search: dict, size: int = 720, episode: int = None):
    for entry in feed['entries']:
        title = guessit(entry['title'])
        name = title.get('title')
        if title.get('screen_size') == f'{size}p':
            for lang in ['english', 'romaji']:
                if search.get(lang):
                    search_guess = guessit(search.get(lang))
                    lookup = search_guess.get('title')
                    ratio = fuzz.token_set_ratio(name, lookup)
                    if ratio > 75:
                        logger.info(
                            f"[PARSER] Found {ratio * 100:2f}% RSS match for Anime: '{name}' ({lang} title) "
                            f"E{title.get('episode')}"
                        )
                        if not episode:
                            return entry['link'], name
                        if title.get('episode'):
                            if title.get('season'):
                                if search_guess.get('season'):
                                    if title.get('season') != search_guess.get('season'):
                                        logger.info(
                                            f"[PARSER] Not returning entry: '{name}' "
                                            f"({lang} title). ({ratio * 100:2f}% match)"
                                            f"Season doesn't match (Wanted: {search_guess.get('season')}, "
                                            f"Found: {title.get('season')})"
                                        )
                                        continue
                            if int(title.get('episode')) == episode:
                                return entry['link'], name
                            logger.info(
                                f"[PARSER] Not returning entry: '{name}' ({lang} title). ({ratio * 100:2f}% match)"
                                f"Episode doesn't match (Wanted: {episode}, Found: {title.get('episode')})"
                            )
    for lang in ['english', 'romaji']:
        if search.get(lang):
            return None, search.get(lang)
