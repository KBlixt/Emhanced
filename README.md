# Emhanced

Improving discoverability in Emby through modifying movies "dateadded" metadata-tag in the nfo files. The result
is a more useful homepage with the Recently added movie tab showing a mix of recently released movies along with a
few random movies that have been selected out of your movies for various reasons. Read the categories section
for more info.

# Installation

clone the repository. 
    git clone https://github.com/KBlixt/Emhanced
edit the "config.cfg-template" to your liking and save it as "config.cfg". read the config section for setting it up correctly.
    nano Emhanced/config.cfg-template
then run it with python3. 
    python3 Emhanced/emhanced.py
    
# Setting up the config

for the script to work you'll need to provide a path to your movie library to the MOVIE_LIBRARY variable. you need
to keep allof your movie folders in the same folder for this script to work. all of your movies must be reachable
with something like /path/to/library/movies/Avatar (2009). in this example you'd provide the
path /path/to/library/movies to the script.

other than that all of the other settings are for colonization. these should be fairly well explained in the config file
and should be fairly straight forward to set up.

in order to enable the "hidden gem" category you'll also need to provide your working tmdb api 3 key. getting a tmdb
api key is dead simple.just make a tmdb account and follow [this guide](https://developers.themoviedb.org/3/getting-started/introduction).

# Categories

there are (for now) 4 categories that you can use. The explanation of these categories will 
contain the default settings, however the order,quantity and other variables of movies in each category can be customized
in the config file. by default the categories will appear in the recently added feed in the same order as here.

### Recently released movies.

this category will provide a list the 3 most recently released movies but if any other movie have been released
within 14 days of the latest movie those will also get added. (maximum 7 in total)

### Old but gold

this category will provide a random movie that is at least 10 years old with a score of at least 7.9.

### hidden gem (need a tmdb api key to enable)

this category will provide a random movie that isn't popular on tmdb and will encourage good scores.

### random

this category will provide a completely random movie

