#!/usr/bin/env python

import sys

import click

from nyaacli.nyaa_search import search_torrent
from nyaacli.colors import red, green


@click.command()
@click.argument('anime')
@click.argument('episode', type=int, default=None, required=False)
@click.option('--output', '-o', default='~/Videos/Anime', help=green('Output Folder'), type=click.Path(), show_default=True)
def main(anime: str, episode: int, output: str):
    """
    Search for an Anime on https://nyaa.si and downloads it

    \b
    Usage:
        \33[92mnyaa-cli \33[36m"Anime Name" \33[33m<Episode Number (Optional)> \33[34m-o <Output Folder (Default = '~/Videos/Anime')>\033[0m

    \b
    Example:
        \33[92mnyaa-cli \33[36m"Kimetsu no Yaiba" \33[33m19 \33[34m-o "My/Animes/Folder/Kimetsu_No_Yaiba/\033[0m
    """
    torrent_search = search_torrent(anime, episode)

    if torrent_search:
        torrent_path, result_name = torrent_search

        download_torrent(torrent_path, result_name, base_path=output)


# if __name__ == '__main__':
try:
    from nyaacli.torrenting import download_torrent
except ModuleNotFoundError:
    print(red("You need to have the 'python3-libtorrent' library installed to run this.\n"))
    print("If you use the apt package manager, you can install with:", green("sudo apt install python3-libtorrent"))

    libtorrent_url = "https://github.com/arvidn/libtorrent/blob/RC_1_2/docs/python_binding.rst"

    print(f"Otherwise, look into how you can build it here: {libtorrent_url}")
    sys.exit(1)

main()
