from guessit import guessit

import logging

logger = logging.getLogger('anime_downloader')


def search_title(feed, search: dict, group: str = 'HorribleSubs', size: int = 720, episode: int = None):
    for entry in feed['entries']:
        title = guessit(entry['title'])
        name = title.get('title')
        if title.get('release_group') == group and title.get('screen_size') == f'{size}p':
            for lang in ['english', 'romaji']:
                if search.get(lang):
                    lookup = guessit(search.get(lang)).get('title')
                    if name == lookup:
                        logger.info(f"[PARSER] Found RSS entry for Anime: '{name}' ({lang} title) E{title.get('episode')}")
                        if not episode:
                            return entry['link'], name
                        if title.get('episode'):
                            if int(title.get('episode')) == episode:
                                return entry['link'], name
                            logger.info(
                                f"[PARSER] Not returning entry: '{name}' ({lang} title). "
                                f"Episode doesn't match (Wanted: {episode}, Found: {title.get('episode')})"
                            )
    for lang in ['english', 'romaji']:
        if search.get(lang):
            return None, search.get(lang)
