import os
import sys
import time
import logging

import libtorrent

from nyaacli.colors import red, green
from nyaacli.utils import clear_screen

logger = logging.getLogger('nyaa')


def download_torrent(filename: str, result_filename: str = None, show_progress: bool = True, base_path: str = 'Anime'):
    session = libtorrent.session({'listen_interfaces': '0.0.0.0:6881'})
    logger.debug('Started libtorrent session')

    base_path = os.path.expanduser(base_path)
    logger.debug(f'Downloading output to: \'{base_path}\'')

    info = libtorrent.torrent_info(filename)

    logger.debug('Started downloading torrent')
    handle: libtorrent.torrent_handle = session.add_torrent({
        'ti': info,
        'save_path': base_path
    })

    status: libtorrent.session_status = handle.status()

    print(f"\n{green('◉ Started downloading torrent:')} {status.name}", end='\n\n')

    if show_progress:
        while not status.is_seeding:
            status = handle.status()

            progress = green(f"{status.progress * 100:.2f}%")
            download_rate = green(f"{status.download_rate / 1000:.1f} kB/s")

            print(
                f'◉ {green(str(status.state).title())} - {progress} '
                f'(Download: {download_rate} - Upload: {status.upload_rate / 1000:.1f} kB/s - '
                f'Peers: {status.num_peers}) ',
                end='\r'
            )

            alerts = session.pop_alerts()

            alert: libtorrent.alert
            for alert in alerts:
                if alert.category() & libtorrent.alert.category_t.error_notification:
                    logger.debug(f"{red('[Alert]')} {alert}")

            sys.stdout.flush()

            time.sleep(1)

        print(green(f'\n\nFinished downloading {handle.name()}'), end='\n\n')

    if result_filename:
        old_name = f'{base_path}/{status.name}'
        new_name = f'{base_path}/{result_filename}'

        os.rename(old_name, new_name)

        clear_screen()

        logger.debug('Finished torrent download')
        print(f'Finished download at: \'{green(new_name)}\' ')


if __name__ == '__main__':
    if len(sys.argv) < 2:
        print('You need to pass in the .torrent file path.')
        sys.exit(1)

    download_torrent(sys.argv[1])
