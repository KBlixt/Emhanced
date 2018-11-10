# Emhanced

Improving discoverability in Emby through modifying movies "dateadded" metadata-tag in the nfo files. The result
is a more useful homepage with the Recently added movie tab showing a mix of recently released movies along with a
few random movies that have been selected out of your movies for various reasons. Read the categories section
for more info.

# Installation (Linux)

### Linux

Clone the repository.
```
git clone https://github.com/KBlixt/Emhanced
```
Edit the "config.cfg-template" to your liking and save it as "config.cfg". Read the config section for setting it up correctly.
```
nano Emhanced/config.cfg-template
```
Then you are done and can run it with python3.
```
python3 Emhanced/emhanced.py
```

#### Other

it really shouldn't be more difficult than clone, configure the config and run it with python3. IF you run into issues,
please let me know.
  
# Setting up the config

For the script to work you'll need to provide a path to your movie library to the MOVIE_LIBRARY variable. You need
to have all of your movie folders in the same folder for this script to work. All of your *movie folders* must be reachable
with something like "/path/to/library/movies/Avatar (2009)". In this example you'd provide the
path "/path/to/library/movies" to the script.

Other than that all of the other settings are for customization. these should be fairly well explained in the config file
and should be fairly straight forward to set up.

In order to enable the "hidden gem" category you'll also need to provide your working tmdb api 3 key. Getting a tmdb
api key is dead simple. Just make a tmdb account and follow [this guide](https://developers.themoviedb.org/3/getting-started/introduction).

# Categories

There are (for now) 4 categories that you can use. The explanation of these categories will
contain the default settings. However the order,quantity and other variables of movies in each category can be customized
in the config file. By default the categories will appear in the recently added feed in the same order as here.

### Recently released movies.

This category will provide a list the 3 most recently released movies but if any other movie have been released
within 14 days of the latest movie those will also get added. (maximum 7 in total)

### Old but gold

This category will provide a random movie that is at least 10 years old with a score of at least 7.9.

### hidden gem (need a tmdb api key to enable)

This category will provide a random movie that isn't popular on tmdb and will encourage good scores.

### random

This category will provide a completely random movie

# Automation

cron example with the script running at 10:30 every day:
```
30 10 * * * /opt/Emhanced/emhanced.py
```

Running it on any kind of scheduler should work fine however. but be aware of that if you have the live monitoring option
enabled on the library it will scan for new and changed files once for every movie this script edits. Either disable 
this or restart the server after the script have finished. 

you'll need to schedule a library scan for a few minutes after this script has been run in order for emby to recognize
the changes 5 minutes should be enough but this will vary from system to system, I'd recommend running it once and see how
long it takes to complete and then double it as a delay just to be safe. Rebooting should do this as well if you choose
to do that instead.

# Feature suggestions

The script is fairly easy to modify and if there are any other feature suggestions they should be fairly quick to
implement. Just open an issue in this repository and I'll have a look at it. Or pm me on Reddit @/u/waraxx