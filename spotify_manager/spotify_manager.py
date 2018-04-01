from spotipy.client import Spotify, SpotifyException
from spotipy import util


class SpotifyManager:
    def __init__(self, username, client_id, client_secret, redirect_uri, scope=None):
        """
                Create a SpotifyManager object.

                :param username: The Spotify Premium username
                :param client_id: The client id of your app
                :param client_secret: The client secret of your app
                :param redirect_uri: The redirect URI of your app
                :param scope: The desired scope of the request
        """
        if not scope:
            scope = 'playlist-read-private playlist-read-collaborative streaming user-library-read ' \
                    'user-library-modify user-read-private user-top-read user-read-playback-state ' \
                    'user-modify-playback-state user-read-currently-playing user-read-recently-played'
        token = util.prompt_for_user_token(username, scope, client_id, client_secret, redirect_uri)
        self.sp = Spotify(auth=token)

    # Player

    def play(self, context=None, uris=None, device=None):
        """
                Start or resume user’s playback.

                Provide a context_uri to start playback or a album, artist, or playlist.

                Provide a uris list to start playback of one or more tracks.

                Don't use context and uris at the same time.

                :param context: Album, artist, or playlist.
                :param uris: List of one or more tracks.
                :param device: The device target.
        """
        try:
            self.sp.start_playback(device, context, uris)
        except SpotifyException as se:
            # Err 403 - Not paused
            if se.http_status != 403:
                raise

    def pause(self, device=None):
        """
                Pause user’s playback.

                :param device: The device target.
        """
        try:
            self.sp.pause_playback(device)
        except SpotifyException as se:
            # Err 403 - Already paused
            if se.http_status != 403:
                raise

    def play_pause(self, device=None):
        """
                Switch between Play and Pause.

                :param device: The device target.
        """
        try:
            self.sp.start_playback(device)
        except SpotifyException as se:
            # Err 403 - Not paused
            if se.http_status == 403:
                self.sp.pause_playback(device)
            else:
                raise

    def next_track(self, device=None):
        """
                Moves to the next track.

                :param device: The device target.
        """
        self.sp.next_track(device)

    def previous_track(self, device=None):
        """
                Moves to the previous track.

                Restart current track if there is no previous track.

                :param device: The device target.
        """
        try:
            self.sp.previous_track(device)
        except SpotifyException as se:
            # Err 403 - No previous track
            if se.http_status == 403:
                self.repeat_track(device)
            else:
                raise

    def repeat_track(self, device=None):
        """
                Restart current track.

                :param device: The device target.
        """
        self.sp.seek_track(0, device)

    def get_shuffle(self):
        """
                Returns the status of the shuffle mode.

                Can be True or False (enabled or disabled).
        """
        return self.sp.current_playback()['shuffle_state']

    def set_shuffle(self, state, device=None):
        """
                Sets the status of the shuffle mode.

                Can be True or False (enabled or disabled).

                :param state: The new shuffle mode.

                :param device: The device target.
        """
        if state in [True, False]:
            self.sp.shuffle(state, device)
        else:
            raise AttributeError('State must be True or False')

    def get_repeat(self):
        """
                Returns the status of the repeat mode.

                Can be track, context or off.
        """
        return self.sp.current_playback()['repeat_state']

    def set_repeat(self, state, device=None):
        """
                Sets the status of the repeat mode.

                Can be track, context or off.

                :param state: The new repeat mode.

                :param device: The device target.
        """
        if state in ['track', 'context', 'off']:
            self.sp.repeat(state, device)
        else:
            raise AttributeError('State must be track, context or off')

    def get_volume(self, device=None):
        """
                Gets current device's volume in percentage.

                If there is no device, returns the volume of the device
                that is active right now.

                :param device: The device target.
        """
        if device:
            dev = self.get_device(device)
        else:
            dev = self.get_active_device()
        return dev['volume_percent']

    def add_volume(self, volume_percent, device=None):
        """
                Increases device's volume in percentage.

                Also works with negative numbers.

                :param volume_percent: The device target

                :param device: The device target
        """
        volume = self.get_volume(device) + volume_percent
        if volume > 100:
            volume = 100
        elif volume < 0:
            volume = 0
        self.set_volume(volume, device)

    def set_volume(self, volume_percent, device=None):
        """
                Sets device's volume in percentage.

                Also works with negative numbers.

                :param volume_percent: The device target

                :param device: The device target
        """
        if 0 <= int(volume_percent) <= 100:
            self.sp.volume(int(volume_percent), device)
        else:
            raise AttributeError('Volume must be an Integer between 0 and 100')

    # Search
    def search_track(self, query, limit=10):
        """
                Search list of tracks that match the query.

                Result -> {'tracks':[{name, artists, album, uri}, ... ]}

                :param query: The search query

                :param limit: Number of results to show
        """
        tracks = {'tracks': []}
        for result in self.sp.search(query, limit, type='track')['tracks']['items']:
            artists_string = ''
            for artist in result['artists']:
                artists_string += artist['name'] + ', '
            tracks['tracks'].append({'name': result['name'], 'artists': artists_string[:-2],
                                     'album': result['album']['name'], 'uri': result['uri']})
        return tracks

    def search_artist(self, query, limit=10):
        """
                Search list of artists that match the query.

                Result -> {'artists': [{name, uri}, ... ]}

                :param query: The search query

                :param limit: Number of results to show
        """
        artists = {'artists': []}
        for artist in self.sp.search(query, limit, type='artist')['artists']['items']:
            artists['artists'].append([artist['name'], artist['uri']])
        return artists

    def search_album(self, query, limit=10):
        """
                Search list of albums that match the query.

                Result -> {'albums': [name, artists, uri], ... }

                :param query: The search query

                :param limit: Number of results to show
        """
        albums = {'albums': []}
        for album in self.sp.search(query, limit, type='album')['albums']['items']:
            artists_string = ''
            for artist in album['artists']:
                artists_string += artist['name'] + ', '
            albums['albums'].append([album['name'], artists_string[:-2], album['uri']])
        return albums

    def search_playlist(self, query, limit=10):
        """
                Search list of playlists that match the query.

                Result -> {'playlists': [name, uri], ... }

                :param query: The search query

                :param limit: Number of results to show
        """
        playlists = {'playlists': []}
        for p in self.sp.search(query, limit, type='playlist')['playlists']['items']:
            playlists['playlists'].append([p['name'], p['uri']])
        return playlists

    # Get data
    def get_current_status(self):
        """
                Return the status of the current user.

                Includes username, track, artists, album and playlist.

                Result -> {username, track: {name, uri}, artists: {all, main, main_uri}, album: {name, uri},
                           playlist: {is_active, uri}}

                Raises ConnectionError if user is not connected.
        """
        status = self.sp.currently_playing()
        if not status:
            raise ConnectionError('User not connected to Spotify ')
        song = status['item']
        album = song['album']
        artists_string = ''
        owners_string = ''
        main_artist = song['artists'][0]
        for artist in song['artists']:
            artists_string += artist['name'] + ', '
        for artist in album['artists']:
            owners_string += artist['name'] + ', '
        playlist_active = False
        playlist_uri = None
        if status['context'] and status['context']['type'] == 'playlist':
            playlist_active = True
            playlist_uri = status['context']['uri']
        return {'username': self.sp.current_user()['id'], 'track': {'name': owners_string[:-2] + ' - ' +
                song['name'], 'uri': song['uri']}, 'artists': {'all': artists_string[:-2],
                'main': {'name': main_artist['name'], 'uri': main_artist['uri']}}, 'album': {'name': album['name'],
                'uri': album['uri']}, 'playlist': {'is_active': playlist_active, 'uri': playlist_uri}}

    def get_playlists(self):
        """
                Returns list of user playlists

                Result -> {'playlists': [name, uri], ... }
        """
        playlists = {'playlists': []}
        for p in self.sp.current_user_playlists()['items']:
            playlists['playlists'].append([p['name'], p['uri']])
        return playlists

    def get_recently_played(self, limit=50):
        """
                Returns list of tracks recently played by the current user.

                Result -> {'tracks':[{name, artists, album, uri}, ... ]}

                :param limit: Number of results to show
        """
        tracks = {'tracks': []}
        for item in self.sp.current_user_recently_played(limit)['items']:
            track = item['track']
            artists_string = ''
            for artist in track['artists']:
                artists_string += artist['name'] + ', '
            tracks['tracks'].append({'name': track['name'], 'artists': artists_string[:-2],
                                     'album': track['album']['name'], 'uri': track['uri']})
        return tracks

    def get_saved_albums(self, limit=20, offset=0):
        # returns dict -> {'albums': [name, artists, uri], ... }
        albums = {'albums': []}
        for item in self.sp.current_user_saved_albums(limit, offset)['items']:
            artists_string = ''
            for artist in item['album']['artists']:
                artists_string += artist['name'] + ', '
            albums['albums'].append([item['album']['name'], artists_string[:-2], item['album']['uri']])
        return albums

    def get_saved_tracks(self, limit=20, offset=0):
        """
                Returns list of tracks saved by the current user.

                Result -> {'tracks':[{name, artists, album, uri}, ... ]}

                :param limit: Number of results to show

                :param offset: Index of the first item to return
        """
        tracks = {'tracks': []}
        for track in self.sp.current_user_saved_tracks(limit, offset)['items']:
            artists_string = ''
            for artist in track['artists']:
                artists_string += artist['name'] + ', '
            tracks['tracks'].append({'name': track['name'], 'artists': artists_string[:-2],
                                     'album': track['album']['name'], 'uri': track['uri']})
        return tracks

    def get_user_top_artists(self, limit=10):
        # returns dict -> {'artists': [{name, uri}, ... ]}
        artists = {'artists': []}
        for artist in self.sp.current_user_top_artists(limit)['items']:
            artists['artists'].append({'artists': artist['name'], 'uri': artist['uri']})
        return artists

    def get_user_top_tracks(self, limit=10):
        """
                Returns list of tracks more played by the current user.

                Result -> {'tracks':[{name, artists, album, uri}, ... ]}

                :param limit: Number of results to show
        """
        tracks = {'tracks': []}
        for track in self.sp.current_user_top_tracks(limit)['items']:
            artists_string = ''
            for artist in track['artists']:
                artists_string += artist['name'] + ', '
            tracks['tracks'].append({'name': track['name'], 'artists': artists_string[:-2],
                                     'album': track['album']['name'], 'uri': track['uri']})
        return tracks

    def get_artist_top_tracks(self, artist_uri, limit=5):
        # returns dict -> {'tracks':[{name, artists, album, uri}, ... ]}
        tracks = {'tracks': []}
        tracks_found = 0
        for track in self.sp.artist_top_tracks(artist_uri)['tracks']:
            tracks['tracks'].append({'name': track['name'], 'artists': self.sp.artist(artist_uri)['uri'],
                                     'album': track['album']['name'], 'uri': track['uri']})
            tracks_found += 1
            if tracks_found >= limit:
                break
        return tracks

    def get_related_artist_tracks(self, artist_uri, max_artists=5, tracks_per_artist=5):
        """
                Returns list of tracks related to an artist.

                It search the top songs of some related artists.

                Result -> {'tracks':[{name, artists, album, uri}, ... ]}

                :param artist_uri: ID of the artist.

                :param max_artists: Number of related artists to show.

                :param tracks_per_artist: Number of tracks per artist to show.
        """
        tracks = {'tracks': []}
        artists_found = 0
        for artist in self.sp.artist_related_artists(artist_uri)['artists']:
            tracks_found = 0
            for track in self.sp.artist_top_tracks(artist['uri'])['tracks']:
                tracks['tracks'].append({'name': track['name'], 'artists': artist,
                                         'album': track['album']['name'], 'uri': track['uri']})
                tracks_found += 1
                if tracks_found >= tracks_per_artist:
                    break
            artists_found += 1
            if artists_found >= max_artists:
                break

        return tracks

    # Set data
    def save_tracks(self, tracks=None):
        """
            Saves one or more tracks on the current user's library

            Tracks is a list similar to [track1.uri, track2.uri, ... ]

            :param tracks: List of uri's tracks to save
        """
        self.sp.current_user_saved_tracks_add(tracks)

    def delete_tracks(self, tracks=None):
        """
            Deletes one or more tracks from the current user's library

            Tracks is a list similar to [track1.uri, track2.uri, ... ]

            :param tracks: List of uri's tracks to delete
        """
        self.sp.current_user_saved_tracks_delete(tracks)

    def save_albums(self, albums=None):
        """
            Saves one or more albums on the current user's library

            Tracks is a list similar to [album1.uri, album2.uri, ... ]

            :param albums: List of uri's albums to save
        """
        if albums is None:
            albums = []
        self.sp.current_user_saved_albums_add(albums)

    # Use data
    def save_current_track(self):
        """
            Saves the track that the current user is playing on it's library
        """
        self.save_tracks([self.get_current_status()['track']['uri']])

    def delete_current_track(self):
        """
            Deletes the track that the current user is playing from it's library
        """
        self.delete_tracks([self.get_current_status()['track']['uri']])

    def save_current_album(self):
        """
            Saves the album that the current user is playing on it's library
        """
        self.save_albums([self.get_current_status()['album']['uri']])

    def play_user_top_artists(self, artists=10, tracks_per_artists=5, shuffle=True, device=None):
        self.pause(device)
        tracks = []
        for artist in self.get_user_top_artists(artists)['artists']:
            for track in self.get_artist_top_tracks(artist['uri'], tracks_per_artists)['tracks']:
                tracks.append(track['uri'])
        self.play(uris=tracks, device=device)
        self.set_shuffle(shuffle)

    def play_user_top_tracks(self, limit=10, shuffle=True, device=None):
        self.pause(device)
        tracks = []
        for track in self.get_user_top_tracks(limit)['tracks']:
            tracks.append(track['uri'])
        self.play(uris=tracks, device=device)
        self.set_shuffle(shuffle)

    def play_recently_played(self, limit=50, shuffle=True, device=None):
        self.pause(device)
        tracks = []
        for track in self.get_recently_played(limit)['tracks']:
            tracks.append(track['uri'])
        self.play(uris=tracks, device=device)
        self.set_shuffle(shuffle)

    def play_current_artist_related_tracks(self, max_artists=5, tracks_per_artist=5, shuffle=True, device=None):
        self.pause(device)
        artist_uri = self.get_current_status()['artists']['main']['uri']
        tracks = []
        for track in self.get_related_artist_tracks(artist_uri, max_artists, tracks_per_artist)['tracks']:
            tracks.append(track['uri'])
        self.play(uris=tracks, device=device)
        self.set_shuffle(shuffle)

    # Devices
    def get_available_devices(self):
        """
                Returns a dict of all the devices available of the current user.

                Result -> {'devices': [{name, id}, ... ]}
        """
        devices = {'devices': []}
        for dev in self.sp.devices()['devices']:
            devices['devices'].append([dev['name'].capitalize(), dev['id']])
        return devices

    def get_active_device(self):
        """
                Returns device dict (see Spotipy docs) from the active device.
        """
        for dev in self.sp.devices()['devices']:
            if dev['is_active']:
                return dev

    def get_device(self, device_id):
        """
                Returns device dict (see Spotipy docs) from a device ID.

                :param device_id: The device target identifier
        """
        for dev in self.sp.devices()['devices']:
            if dev['id'] == device_id:
                return dev
