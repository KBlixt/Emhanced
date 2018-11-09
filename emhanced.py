import os
import configparser
import recentaddedmod as recent
from random import shuffle
import embyinterface as database
os.chdir(os.path.dirname(os.path.realpath(__file__)))

configfile = 'config.cfg'
cfg = configparser.ConfigParser()
cfg.read(configfile)
config = cfg['GENERAL_SETTINGS']

# if len(api_key) < 5:
#     print('No TMDB API key provided.')
api_key = config.get('tmdb_api_key', '')
mod_list = list()

config = cfg['MOVIES_SETTINGS']
movies = database.get_movies(config.get('MOVIE_LIBRARY'))

movies.sort(key=lambda x: x['releasedate'], reverse=True)

config = cfg['RECENT_RELEASES']
if config.getint('MAX_COUNT') > 0:
    mod_list.append([config.getint('ORDER')] + recent.recent_releases(movies,
                                                               config.getint('MIN_COUNT'),
                                                               config.getint('MAX_COUNT'),
                                                               config.getint('DAY_LIMIT')))

shuffle(movies)

config = cfg['OLD_BUT_GOLD']
if config.getint('COUNT') > 0:
    mod_list.append([config.getint('ORDER')] + recent.old_but_gold(movies,
                                                                  config.getint('COUNT'),
                                                                  config.getfloat('YEAR_LIMIT'),
                                                                  config.getfloat('MIN_CRITIC_SCORE')))

config = cfg['HIDDEN_GEM']
if config.getint('COUNT') > 0:
    if len(api_key) < 5:
        print('No TMDB API key provided.')
    else:
        mod_list.append([config.getint('ORDER')] + recent.hidden_gem(movies, config.getint('COUNT'), api_key))

config = cfg['RANDOM']
if config.getint('COUNT') > 0:
    mod_list.append([config.getint('ORDER')] + recent.random(movies, config.getint('COUNT')))

database.edit_database(mod_list)
print('done')
