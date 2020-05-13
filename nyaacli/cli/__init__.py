#!/usr/bin/env python

import logging
import sys

from nyaacli.nyaa_search import search_torrent
from nyaacli.colors import red, green
from nyaacli.logger import CustomFormatter

import click
from colorama import init

init()


@click.command()
@click.argument('anime')
@click.argument('episode', type=int, default=None, required=False)
@click.option('--output', '-o', default='~/Videos/Anime', help=green('Output Folder'), type=click.Path(), show_default=True)
@click.option('--debug/--no-debug', default=False, help=green('Debug Mode'))
@click.option('--number', '-n', default=10, help=green('Number of entries'), show_default=True)
def main(anime: str, episode: int, output: str, debug: bool = False, number: int = 10):
    """
    Search for Anime on https://nyaa.si and downloads it

    \b
    Usage:
        \33[92mnyaa \33[36m"Anime Name" \33[33m<Episode Number (Optional)> \33[34m-o <Output Folder (Default = '~/Videos/Anime')>\033[0m

    \b
    Example:
        \33[92mnyaa \33[36m"Kimetsu no Yaiba" \33[33m19 \33[34m-o /home/user/My/Animes/Folder/Kimetsu_No_Yaiba/\033[0m
    """
    # Setup debugging
    logger = logging.getLogger("nyaa")
    logger.setLevel(logging.CRITICAL)

    ch = logging.StreamHandler()
    ch.setLevel(logging.CRITICAL)
    ch.setFormatter(CustomFormatter())

    logger.addHandler(ch)

    if debug:
        # Add debugging logging in debug mode
        logger.setLevel(logging.DEBUG)
        ch.setLevel(logging.DEBUG)

    torrent_search = search_torrent(anime, episode, number=number)

    if torrent_search:
        torrent_path, result_name = torrent_search

        download_torrent(torrent_path, result_name, base_path=output)


try:
    from nyaacli.torrenting import download_torrent
except ModuleNotFoundError:
    print(red("You need to have the 'python3-libtorrent' library installed to user nyaa-cli.\n"))

    aur_url = 'https://aur.archlinux.org/packages/libtorrent-rasterbar-git'

    print('- Install with Apt:', green('sudo apt install python3-libtorrent'))
    print('- Install from the AUR:', green(aur_url))

    libtorrent_url = "https://github.com/arvidn/libtorrent/blob/RC_1_2/docs/python_binding.rst"

    print(f"\nOtherwise, look into how you can build it here: {libtorrent_url}")
    sys.exit(1)

main()
