from datetime import date
from datetime import timedelta
import json
from urllib.request import urlopen
from urllib.error import HTTPError, URLError
from _socket import timeout
import time
from random import shuffle


def get_tmdb_details_data(lang, api_key, tmdb_id):
    response = retrieve_web_page('https://api.themoviedb.org/3/movie/'
                                 + tmdb_id +
                                 '?api_key=' + api_key +
                                 '&language=' + lang, 'movie details')
    if response is None:
        return None
    data = json.loads(response.read().decode('utf-8'))
    response.close()

    return data


def retrieve_web_page(url, page_name='page'):

    response = None
    print('Downloading ' + page_name + '.')

    for tries in range(1, 10):
        try:
            response = urlopen(url, timeout=2)
            break

        except UnicodeEncodeError as e:
            print('Failed to download ' + page_name + ' : ' + str(e) + '. Skipping.')
            break

        except timeout:
            if tries > 5:
                print('You might have lost internet connection.')
                break

            time.sleep(1)
            print('Failed to download ' + page_name + ' : timed out. Retrying.')

        except HTTPError as e:
            print('Failed to download ' + page_name + ' : ' + str(e) + '. Skipping.')
            break

        except URLError:
            if tries > 3:
                print('You might have lost internet connection.')
                raise

            time.sleep(1)
            print('Failed to download ' + page_name + '. Retrying.')

    return response


def recent_releases(items, minimum, maximum, day_limit):
    items.sort(key=lambda x: x['releasedate'], reverse=True)
    local_mod_list = list()
    count = 0
    most_recent_date = items[0]['releasedate']

    for item in items[:maximum]:

        if count < minimum:
            local_mod_list.append(item)
            items.remove(item)
            count += 1

        elif item['releasedate'] > (most_recent_date - timedelta(days=day_limit)):
            local_mod_list.append(item)
            items.remove(item)
            count += 1
        else:
            break

    return local_mod_list


def old_but_gold(items, maximum, age_limit, score_limit):
    shuffle(items)
    local_mod_list = list()
    count = 0
    for item in items:

        con1 = item['rating'] >= score_limit
        con2 = item['releasedate'] < date.today() - timedelta(days=365*age_limit)
        if con1 and con2:
            local_mod_list.append(item)
            items.remove(item)
            count += 1

        if count >= maximum:
            break

    return local_mod_list


def hidden_gem(items, maximum, api_key):
    shuffle(items)
    local_mod_list = list()

    for item in items[:2 + 6 * maximum]:
        tmdb_data = get_tmdb_details_data('en-US', api_key, item['tmdbid'])
        if tmdb_data is None:
            continue
        item['adjusted_popularity'] = float(tmdb_data['popularity']) * \
                                           (1.05 ** ((date.today() - timedelta(days=1095)).year -
                                                     item['releasedate'].year)) * \
                                           (1 / (item['rating'] ** 1.2))

        local_mod_list.append(item)

    local_mod_list.sort(key=lambda x: x['adjusted_popularity'], reverse=True)

    for item in local_mod_list[:maximum]:
        items.remove(item)
    return local_mod_list[:maximum]


def random(items, maximum):
    shuffle(items)
    local_mod_list = list()

    for item in items[:maximum]:
        local_mod_list.append(item)
        items.remove(item)
    return local_mod_list
