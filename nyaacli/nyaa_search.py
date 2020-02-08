from questionary import prompt
from guessit import guessit

from nyaacli.colors import red, green, prompt_style

from urllib import request
from typing import Optional, List, Tuple
from dataclasses import dataclass
from datetime import datetime
from time import mktime
import feedparser
import sys
import os

os.environ['REGEX_DISABLED'] = '1'


def get_file_extension(path: str) -> str:
    """
    Gets the File extension from the path to a file

    'asd.txt' -> '.txt'
    'asd' -> ''
    '/path/to/asd.mkv' -> '.mkv'
    """
    filename, extension = os.path.splitext(path)

    return extension


def text_break() -> None:
    print('-' * 10, end='\n')


@dataclass
class Entry:
    title: str
    link: str
    original_title: str
    extension: str
    full_title: Optional[str]
    episode: Optional[int]
    other: Optional[str]
    release_group: Optional[str]
    screen_size: Optional[str]
    alternative_title: Optional[str]
    display_title: Optional[str]
    season: Optional[str]
    seeders: Optional[str]
    size: Optional[str]
    episode_title: Optional[str]
    date: datetime


def search_torrent(search: str, episode: Optional[int] = None, dub: bool = False) -> Optional[Tuple[str, str]]:
    """
    Results a tuple with (Path to .torrent file, Result name of video file)
    Nyaa.si rss search flags
    https://github.com/nyaadevs/nyaa/blob/a38e5d5b53805ecb1d94853d849826f948f07aad/nyaa/views/main.py#L65
    """

    search_query = f'{search}'.strip().replace(' ', '%20')
    if episode:
        search_query += f' {episode}'.strip().replace(' ', '%20')

    search_url = f'https://nyaa.si/rss?c=1_2&q={search_query}&s=seeders&o=desc'

    # Parse Nyaa.si rss feed search
    feed: feedparser.FeedParserDict = feedparser.parse(search_url)

    if not feed.entries and feed.bozo_exception:
        # Malformatted feed
        print(red(f"[Error] {str(feed.bozo_exception)}"))
        sys.exit(1)

    entries: List[Entry] = []

    for entry in feed.entries:
        title = guessit(entry['title'])

        if not title.get('screen_size'):
            # Ignore entries without Screen size property
            continue

        if not dub and 'dub' in entry['title'].lower():
            # Ignore entries with 'dub' in their titles if dub=False
            continue

        # Screen size needs to be higher than 480p
        good_size = int(title.get('screen_size').replace('p', '')) > 480

        if (title.get('episode') == episode or not episode) and title.get('type') == 'episode' and good_size:
            entries.append(Entry(
                link=entry['link'],
                size=entry['nyaa_size'],
                original_title=entry['title'],
                display_title=entry['title'],
                extension=get_file_extension(entry['title']),
                title=title.get('title'),
                season=title.get('season'),
                seeders=entry.get('nyaa_seeders'),
                full_title='',
                episode=title.get('episode'),
                episode_title=title.get('episode_title'),
                other=title.get('other'),
                release_group=title.get('release_group'),
                screen_size=title.get('screen_size'),
                alternative_title=title.get('alternative_title'),
                date=datetime.fromtimestamp(mktime(entry.get('published_parsed')))
            ))

    if not entries:
        print(red(f'No results found for search: \'{search_query.replace("%20", " ")}\''))
        return None

    for entry in entries[:5]:
        entry_title = entry.title
        entry.full_title = entry.title

        if entry.alternative_title:
            entry_title += f' - {entry.alternative_title}'
            entry.full_title += f' - {entry.alternative_title}'

        if entry.episode or entry.episode_title:
            if entry.episode:
                entry_title += f' - Episode {entry.episode}'
                entry.full_title += f' - Episode {entry.episode}'
            else:
                entry_title += f' - Episode {entry.episode_title}'
                entry.full_title += f' - Episode {entry.episode_title}'

        if entry.season:
            entry_title += f' - Season {entry.season}'
            entry.full_title += f' - Season {entry.season}'

        if entry.release_group:
            entry_title += f' ({entry.release_group})'

        if entry.screen_size:
            entry_title += f' {entry.screen_size}'

        if entry.seeders:
            seeders = f'{entry.seeders} Seeders'
            entry_title += f' - {seeders}'

        if entry.size:
            entry_title += f' - {entry.size}'

        if entry.date:
            entry_title += f" ({entry.date.strftime('%d/%m/%y')})"

        entry.display_title = entry_title

    choices = [{'name': entry.display_title, 'value': index} for index, entry in enumerate(entries[:5])]

    questions = [
        {
            'type': 'list',
            'choices': choices,
            'name': 'selection',
            'message': 'Select one of the entries below',
        }
    ]

    answer = prompt(questions, style=prompt_style)

    if not answer:
        # Cancelled with Ctrl + C
        sys.exit(0)

    index_choice = answer['selection'] - 1

    entry_choice = entries[index_choice]

    final_path = entry_choice.full_title

    torrent_path = f'/tmp/{final_path}.torrent'

    print(f"{green('[Downloading Torrent File]')} '{torrent_path}'")

    request.urlretrieve(entry_choice.link, torrent_path)

    return torrent_path, final_path + entry_choice.extension
