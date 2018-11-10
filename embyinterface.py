import os
import glob
import codecs
from datetime import date
from datetime import datetime
from datetime import timedelta


def get_movies(movie_library_dir):
    print('Reading nfo files, this could take a few minutes.')
    items = list()

    for movie_folder in os.listdir(movie_library_dir):

        for filename in glob.glob(os.path.join(movie_library_dir, movie_folder, '*.nfo')):

            item = {'folder': movie_folder}
            with codecs.open(filename, 'r', 'utf-8') as file:
                try:
                    nfo = file.read()
                    item['nfo_file'] = filename
                except UnicodeDecodeError:
                    print('Something went wrong reading the nfo file of "' + filename + '"')
                    print('Skipping that file')
                    continue

            nfo = nfo.split('\n')
            for line in nfo:
                if '<releasedate>' in line:
                    line = line.replace('<releasedate>', '').replace('</releasedate>', '').split('-')
                    movie_date = date(int(line[0]), int(line[1]), int(line[2]))
                    item['releasedate'] = movie_date

                elif '<rating>' in line:
                    line = line.replace('<rating>', '').replace('</rating>', '')
                    item['rating'] = float(line)

                elif '<criticrating>' in line:
                    line = line.replace('<criticrating>', '').replace('</criticrating>', '')
                    item['criticrating'] = float(line)

                elif '<tmdbid>' in line:
                    line = line.replace('<tmdbid>', '').replace('</tmdbid>', '').strip()
                    item['tmdbid'] = line

            items.append(item)

    return items


def edit_database(mod_list):
    mod_list.sort(key=lambda x: x[0])
    for mod in mod_list:
        mod.pop(0)
    now = datetime.now() + timedelta(days=1)

    for mod in mod_list:
        for item in mod:
            now = now - timedelta(seconds=1)
            with codecs.open(item['nfo_file'], 'r', 'utf-8') as file:
                try:
                    nfo = file.read()
                except UnicodeDecodeError:
                    print('something went wrong reading the nfo file of "' + item['nfo_file'] + '".')
                    continue
            nfo = nfo.split('\n')
            count = 0
            for line in nfo:
                if '<dateadded>' in line:
                    nfo[count] = '  <dateadded>' + now.isoformat().replace('T', ' ')[:-7] + '</dateadded>'
                    break
                count += 1

            print('editing the added date for the movie "' + item['folder'] + '"')
            nfo = '\n'.join(nfo)
            with codecs.open(item['nfo_file'], 'w', 'utf-8') as file:
                try:
                    file.write(nfo)
                except UnicodeEncodeError:
                    print('something went wrong writing to the file "' + item['nfo_file'] + '"')
