# SPOTIFY-MANAGER

## Description

spotify-manager is a Python 3 library wrote to simplify the basic usage of Spotipy

## Installation (On work)

If you already have [Python3](http://www.python.org/) on your system you can install the library simply by downloading the distribution, unpack it and install in the usual fashion:

```bash
python3 setup.py install
```

You can also install it using a popular package manager with

```bash
pip3 install spotify-manager
```

or

```bash
easy_install spotify-manager
```

## Dependencies

- [Spotipy](https://github.com/plamere/spotipy) - spotify-account requires spotipy to be installed
- [Requests](https://github.com/kennethreitz/requests) - spotipy requires the requests package to be installed
- Spotify Premium - premium is required to use the library


## Quick Start

To get started, simply install spotify-account, create a spotifyAccount object and call methods:

```python
from spotify_manager import SpotifyManager
sm = SpotifyManager(SPOTIFY_USERNAME, SPOTIFY_CLIENT_ID, 
                                    SPOTIFY_CLIENT_SECRET, SPOTIFY_REDIRECT_URI)

sm.play_song('eminem mockingbird')
# Mockingbird - Eminem is now running on your device

print(sm.get_current_song_info())
>>> {'name': 'Eminem - Mockingbird', 'uri': 'spotify:track:17baAghWcrewNOcc9dCewx'}, 
    'artists': {'all': 'Eminem', 'main': {'name': 'Eminem', 
    'uri': 'spotify:artist:7dGJo4pcD2V6oG8kP0tJRR'}}, 'album': {'name': 
    'Curtain Call (Deluxe)', 'uri': 'spotify:album:71xFWYFtiHC8eP99QB30AA'}, 
    'playlist': {'is_active': False, 'uri': None}}

sm.play_similar_from_current_artist()
# My Band - D12 is now running on your device, followed by a list of another 19 related songs (customizable)
```

## Documentation

https://spotify-manager.readthedocs.io/en/latest/

## Reporting Issues

If you have suggestions, bugs or other issues specific to this library, file them [here](https://github.com/WolfyLPDC/spotify-manager/issues). Or just send me a pull request.

## Version

- 1.0 - 17/03/2018 - Initial release.
- 1.1 - 27/03/2018 - Added some new methods and revised the old ones.
- 1.2 - 20/03/2018 - Added some new methods and revised the old ones.
- 1.3 - 4/05/2018 - All methods are redone, increasing transparency level. 
