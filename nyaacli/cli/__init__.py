#!/usr/bin/env python

import logging
import sys
from typing import List

from rich import print
from rich.logging import RichHandler
from rich.traceback import install

from nyaacli.nyaa_search import search_torrent
from nyaacli.colors import green
from nyaacli.utils import xdg_open

import click
from colorama import init

init()
install(show_locals=True)


def entries_autocomplete(ctx, args: List[str], incomplete: str):
    """
    Auto-complete choices for --number / -n argument
    """

    text = 'Selection Entries'

    entries = [
        ('5', f'5 {text}'),
        ('10', f'10 {text} (default)'),
        ('15', f'15 {text}'),
        ('20', f'20 {text}')
    ]

    return [c for c in entries if incomplete in c[0]]


def sort_mode_autocomplete(ctx, args: List[str], incomplete: str):
    """
    Auto-complete choices for --sort-by / -s argument
    """

    entries = [
        ('seeders', 'Sort by number of torrent seeders (default)'),
        ('date', 'Sort by upload date'),
        ('size', 'Sort by file size'),
        ('comments', 'Sort by number of comments')
    ]

    return [c for c in entries if incomplete in c[0]]


@click.command()
@click.argument('anime')
@click.argument('episode', type=int, default=None, required=False)
@click.option('--output', '-o', default='~/Videos/Anime', help=green('Output Folder'), type=click.Path(), show_default=True)
@click.option('--number', '-n', default=10, help=green('Number of entries'), show_default=True, autocompletion=entries_autocomplete)
@click.option('--sort-by', '-s', default='seeders', help=green('Sort by'), show_default=True, autocompletion=sort_mode_autocomplete)
@click.option('--trusted', '-t', default=False, help=green('Only search trusted uploads'), is_flag=True)
@click.option('--debug', '-d', default=False, help=green('Debug Mode'), is_flag=True)
@click.option('--client', '-c', default=False, help=green('Use Torrent Client'), is_flag=True)
@click.option('--player', '-p', default=False, help=green('Open in Video Player after download'), is_flag=True)
def main(
    anime: str,
    episode: int,
    output: str,
    debug: bool = False,
    client: bool = False,
    trusted: bool = False,
    player: bool = False,
    number: int = 10,
    sort_by: str = 'seeders',
):
    """
    Search for Anime on https://nyaa.si and downloads it

    \b
    Usage:
        \33[92mnyaa \33[36m"Anime Name" \33[33m<Episode Number (Optional)> \33[34m-o <Output Folder (Default = "~/Videos/Anime")>\033[0m

    \b
    Example:
        \33[92mnyaa \33[36m"Kimetsu no Yaiba" \33[33m19 \33[34m-o /home/user/My/Animes/Folder/Kimetsu_No_Yaiba/\033[0m
    """
    # Setup debugging
    logger = logging.getLogger("nyaa")
    logger.setLevel(logging.CRITICAL)
    logger.addHandler(RichHandler())

    if debug:
        # Add debugging logging in debug mode
        logger.setLevel(logging.DEBUG)

    if not client:
        try:
            from nyaacli.torrenting import download_torrent
        except ModuleNotFoundError:
            print("[bold red]You need to have the 'libtorrent' library (with the Python API) installed to user nyaa-cli.[/bold red]\n")

            print('- Install with apt: [bold green]sudo apt install python3-libtorrent[/bold green]')
            print('- Install with pacman: [bold green]sudo pacman -S libtorrent-rasterbar[/bold green]')

            print('\nAlternatively pass the flag [bold green]--client[/bold green] to use your default torrenting client instead.')
            sys.exit(1)

    torrent_search = search_torrent(anime, episode, number=number, trusted_only=trusted, sort_by=sort_by)

    if torrent_search:
        torrent_path, result_name = torrent_search

        if client:
            xdg_open(torrent_path)
        else:
            output_path = download_torrent(torrent_path, result_name, base_path=output)

            print(f'Finished download at: [green]\'{output_path}\'[/green] ')

            if player:
                xdg_open(output_path)


main()
