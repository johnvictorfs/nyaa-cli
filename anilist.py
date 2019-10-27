import requests
import logging

logger = logging.getLogger('anime_downloader')


def fetch_user_list(username: str, token: str) -> list:
    query = '''
        query ($username: String) {
        MediaListCollection(userName: $username, type: ANIME) {
            lists {
            name
            status
            isCustomList
            entries {
                id
                progress
                status
                repeat
                media{
                id
                type
                format
                status
                source
                season
                episodes
                startDate {
                    year
                    month
                    day
                }
                endDate {
                    year
                    month
                    day
                }
                title {
                    romaji
                    english
                    native
                }
                }
            }
            }
        }
        }
        '''

    variables = {'username': username}

    url = 'https://graphql.anilist.co'

    headers = {
        'Authorization': f'Bearer {token}',
        'Accept': 'application/json',
        'Content-Type': 'application/json'
    }

    response = requests.post(url, headers=headers, json={
                             'query': query, 'variables': variables})
    if response:
        return response.json().get('data').get('MediaListCollection').get('lists')
    return []


def fetch_watching(user_list: list) -> list:
    watching = []
    for item in user_list:
        if item['status'] == 'CURRENT':
            for entry in item['entries']:
                watching.append(entry)
    return watching
