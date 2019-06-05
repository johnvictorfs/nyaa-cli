import logging
import os

from guessit import guessit

logger = logging.getLogger('anime_renamer')
fh = logging.FileHandler('anime_renamer.log')
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
fh.setLevel(logging.INFO)
fh.setFormatter(formatter)
logger.setLevel(logging.INFO)
logger.addHandler(fh)
logger.addHandler(logging.StreamHandler())

if __name__ == '__main__':
    path = f"/home/john/Videos/Anime"
    for file in os.listdir(path):
        guess = guessit(file)

        title = guess.get('title')
        season = f'S{guess.get("season")}' if guess.get("season") else ''
        episode = f'E{guess.get("episode")}' if guess.get("episode") else ''
        container = f'.{guess.get("container")}' if guess.get("container") else ''
        episode_title = f' - {guess.get("episode_title")}' if guess.get("episode_title") else ''

        final = f"{title}{episode_title} {season}{episode}{container}"
        os.rename(f"{path}/{file}", f"{path}/{final}")
        logger.info(f"Renaming {path}/{file} to {path}/{final}")
        logger.info("")
