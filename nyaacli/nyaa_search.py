from rich import print
from rich.progress import Progress, BarColumn, SpinnerColumn
from questionary import prompt
from guessit import guessit

from nyaacli.colors import prompt_style

from urllib import parse, request
from typing import Optional, List, Tuple, Dict
from dataclasses import dataclass
from datetime import datetime
from time import mktime
import feedparser
import logging
import sys
import os
import re

os.environ['REGEX_DISABLED'] = '1'

logger = logging.getLogger('nyaa')


def get_file_extension(path: str) -> str:
    """
    Gets the File extension from the path to a file

    'asd.txt' -> '.txt'
    'asd' -> ''
    '/path/to/asd.mkv' -> '.mkv'
    """
    filename, extension = os.path.splitext(path)
    logger.debug(f"[File Extension] Path: '{path}' -> ('{filename}' + '{extension}')")

    return extension


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

    def __str__(self):
        return (
            f'Entry('
            f'title={repr(self.title)}, '
            f'episode={repr(self.episode)}, '
            f'extension={repr(self.extension)}, '
            f'screen_size={repr(self.screen_size)}'
            f')'
        )


def search_torrent(
    search: str,
    episode: Optional[int] = None,
    dub: bool = False,
    number: int = 10,
    trusted_only: bool = False,
    sort_by: str = 'seeders'


) -> Optional[Tuple[str, str]]:
    """
    Results a tuple with (Path to .torrent file, Result name of video file)
    Nyaa.si rss search flags
    https://github.com/nyaadevs/nyaa/blob/a38e5d5b53805ecb1d94853d849826f948f07aad/nyaa/views/main.py#L65
    """

    search_query = f'{search}'.strip()
    if episode:
        search_query += f' {episode}'

    logger.debug(f'Searching nyaa for query: \'{search_query}\'')

    url_arguments: Dict[str, str] = {
        'c': '1_2',  # Language (English)
        'q': search_query,  # Search Query
    }

    if trusted_only:
        url_arguments['f'] = '2'  # Trusted uploaders only

    # What to sort torrents by
    if sort_by == 'seeders':
        url_arguments['s'] = 'seeders'
    elif sort_by == 'date':
        url_arguments['s'] = 'id'
    elif sort_by == 'size':
        url_arguments['s'] = 'size'
    elif sort_by == 'comments':
        url_arguments['s'] = 'comments'

    logger.debug(f'URL Arguments: {url_arguments}')

    search_url = 'https://nyaa.si/rss?' + parse.urlencode(url_arguments)

    with Progress(SpinnerColumn(), '[progress.description]{task.description}', BarColumn(bar_width=None)) as progress:
        search_task = progress.add_task("[cyan]Searching for anime...", start=False)

        # Parse Nyaa.si rss feed search
        feed: feedparser.FeedParserDict = feedparser.parse(search_url)
        logger.debug(f'Getting feed parse from: \'{search_url}\'')

        if not feed.entries:
            print('[bold red]No entries found for search[/bold red]')
            sys.exit(1)

        entries: List[Entry] = []

        # Find resolution in string regex
        screen_size_pattern = re.compile(r'^([0-9]+)|.?([0-9]{4})p')

        for entry in feed.entries:
            title = guessit(entry['title'])

            if episode:
                if title.get('type') != 'episode':
                    logger.debug(f"Skipping (Not episode, but searching for E{episode}) {entry}")
                    continue

                if title.get('episode') != episode:
                    logger.debug(f"Skipping (Wrong episode, searching for E{episode}) {entry}")
                    continue

            if not dub and 'dub' in entry['title'].lower():
                # Ignore entries with 'dub' in their titles if dub=False
                logger.debug(f"Skipping (Dub) {entry}")
                continue

            size = 0

            # Screen size needs to be higher than 480p
            if title.get('screen_size'):
                sizes = re.search(screen_size_pattern, title.get('screen_size'))
            else:
                sizes = re.search(screen_size_pattern, entry['title'])

            if sizes:
                for group in sizes.groups():
                    if group:
                        size = int(group)

            good_size = size > 480

            if not title.get('screen_size'):
                # Add screen size to title properties if not already there
                title['screen_size'] = f'{size}p'

            if not good_size:
                logger.debug(f"Skipping (bad size ({size})) {entry}")
                continue

            entry = Entry(
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
            )
            logger.debug(f'Added entry: {entry}')
            entries.append(entry)

        if not entries:
            print(f'[bold red]No results found for search: \'{search_query.replace("%20", " ")}\'[/bold red]')
            return None

        for entry in entries[:number]:
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

        choices = [{'name': entry.display_title, 'value': index} for index, entry in enumerate(entries[:number])]

        questions = [
            {
                'type': 'list',
                'choices': choices,
                'name': 'selection',
                'message': 'Select one of the entries below',
            }
        ]

        logger.debug(f'Download choices: {choices}')

        progress.update(search_task, visible=False)

    answer = prompt(questions, style=prompt_style)

    if not answer:
        # Cancelled with Ctrl + C
        sys.exit(0)

    logger.debug(f'Selection: [{answer["selection"]}]')

    index_choice = answer['selection']

    entry_choice = entries[index_choice]

    logger.debug(f'Selected entry at index {index_choice}: {entry_choice}')

    final_path = entry_choice.full_title

    torrent_path = f'/tmp/{final_path}.torrent'
    logger.debug(f'Downloading torrent file to \'{torrent_path}\' from \'{entry_choice.link}\'')

    request.urlretrieve(entry_choice.link, torrent_path)
    logger.debug('Downloaded torrent file')

    logger.debug(f'Final path: {final_path}')
    logger.debug(f'File Extension: {entry_choice.extension}')

    return torrent_path, final_path + entry_choice.extension
