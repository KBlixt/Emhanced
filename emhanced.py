import os
import configparser
import recentaddedmod as recent
from random import shuffle
import embyinterface as database
import sys
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
if os.path.isdir(config.get('MOVIE_LIBRARY')):
    movies = database.get_movies(config.get('MOVIE_LIBRARY'))
else:
    print('Invalid movie library. not a directory.')
    sys.exit()


movies.sort(key=lambda x: x['releasedate'], reverse=True)
try:
    config = cfg['RECENT_RELEASES']
    if config.getint('MAX_COUNT', 7) > 0:
        mod_list.append([config.getint('ORDER', 0)] + recent.recent_releases(movies,
                                                                   config.getint('MIN_COUNT', 3),
                                                                   config.getint('MAX_COUNT', 7),
                                                                   config.getfloat('DAY_LIMIT', 14)))
except ValueError:
    print('Please make sure that you have set up the RECENT_RELEASES category correctly.')
    print('MIN_COUNT: only whole numbers')
    print('MAX_COUNT: only whole numbers')
    print('DAY_LIMIT: only numbers')

shuffle(movies)
try:
    config = cfg['OLD_BUT_GOLD']
    if config.getint('COUNT', 1) > 0:
        mod_list.append([config.getint('ORDER', 1)] + recent.old_but_gold(movies,
                                                                  config.getint('COUNT', 1),
                                                                  config.getfloat('YEAR_LIMIT', 10),
                                                                  config.getfloat('MIN_CRITIC_SCORE', 7.9)))
except ValueError:
    print('Please make sure that you have set up the OLD_BUT_GOLD category correctly.')
    print('COUNT: only whole numbers')
    print('YEAR_LIMIT: only numbers')
    print('MIN_CRITIC_SCORE: only numbers')

try:
    config = cfg['HIDDEN_GEM']
    if config.getint('COUNT', 1) > 0:
        if len(api_key) < 5:
            print('No TMDB API key provided.')
        else:
            mod_list.append([config.getint('ORDER', 2)] + recent.hidden_gem(movies, config.getint('COUNT', 1), api_key))
except ValueError:
    print('Please make sure that you have set up the HIDDEN_GEM category correctly.')
    print('COUNT: only whole numbers')

try:
    config = cfg['RANDOM']
    if config.getint('COUNT', 1) > 0:
        mod_list.append([config.getint('ORDER', 3)] + recent.random(movies, config.getint('COUNT', 1)))
except ValueError:
    print('Please make sure that you have set up the RANDOM category correctly.')
    print('COUNT: only whole numbers')

database.edit_database(mod_list)
print('done')
