.. spotify-manager documentation master file, created by
   sphinx-quickstart on Sun Apr  1 12:44:39 2018.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Welcome to spotify-manager!
===========================
*spotify-manager* is a lightweight Python3 library for the easy use and
integration of `Spotipy <https://github.com/plamere/spotipy>`_ in your projects.
As long as this library is only an upper leveled Spotipy, it still works with
the `Spotify Web API <https://developer.spotify.com/web-api/>`_ and your are
going to need Spotify Premium and an API Token.

The spirit of spotify-manager is to automatize some requests related with the
streaming, but not all of them. Searching data or updating your profile is less
important for this library than playing your fifty last tracks again or repeat a
song. I just focused on the things I find more important and useful.

Here's a quick example of using *spotify-manager* to search and play a track
like for example 'Mockingbird' by 'Eminem'::

    from spotify_manager import SpotifyManager

    sm = SpotifyManager(username, client_id, client_secret, redirect_uri)
    sm.play_song('eminem mockingbird')

Here's another example showing how to play songs related to the artist you
are listening to right now::

    from spotify_manager import SpotifyManager

    sm = SpotifyManager(username, client_id, client_secret, redirect_uri)
    sm.play_similar_from_current_artist()

Finally, here's an example of increasing the volume of the device you are
listening to right now a twenty percent::

    from spotify_manager import SpotifyManager

    sm = SpotifyManager(username, client_id, client_secret, redirect_uri)
    sm.add_volume(20)

As you can see, it's pretty simple to use this library and it's more upper
leveled than `Spotipy <https://github.com/plamere/spotipy>`_, so you don't
have to focus that much on the implementation.

Features
========
*spotify-manager* is a lightweight Python3 library for the easy use and
integration of `Spotipy <https://github.com/plamere/spotipy>`_ in your projects.
As long as this library is only an upper leveled Spotipy, it still works with
the `Spotify Web API <https://developer.spotify.com/web-api/>`_ and your are
going to need Spotify Premium and an API Token.

The spirit of spotify-manager is to automatize some requests related with the
streaming, but not all of them. Searching data or updating your profile is less
important for this library than play your fifty last tracks again or repeat a
song. I just focused on the things I find more important and util.

Installation
============
Install *spotify-manager* with::

    pip3 install spotify-manager

Or with::

    easy_install spotify-manager

Or you can get the source from github at https://github.com/msolefonte/spotify-manager

Authorized requests
===================
As long as this is a library that uses Spotify's API you are going to need
authentication to use it. Because it has the same problems than Spotipy, and
I'm using that library, the best I can do is to link their docs to allow you
to read about this problem (feature).

https://spotipy.readthedocs.io/en/latest/#authorized-requests

API Reference
=============
:mod:`spotify_manager` Module
=============================
.. automodule:: spotify_manager.spotify_manager
    :members:
    :undoc-members:
    :special-members: __init__
    :show-inheritance:

Support
=======
If you any have questions about spotify-manager, you can mail me to my account
*'msolefonte @ gmail.com'* and I will try to answer as soon as possible.

If you think you've found a bug, let me know at
`spotify-manager <https://github.com/msolefonte/spotify-manager/issues>`_


Contribute
==========
spotify-manager authored by Marc Solé (`msolefonte <https://github.com/msolefonte/>`_)
with special thanks to Paul Lamere (`plamere <https://github.com/plamere/>`_),
the author of the great library Spotipy, and to all the people that have contributed to make this possible.

License
=======
https://github.com/msolefonte/spotify-manager/blob/master/LICENSE
