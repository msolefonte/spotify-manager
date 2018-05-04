from spotipy.client import Spotify, SpotifyException
from spotipy import util


class SpotifyManager:
    def __init__(self, username, client_id, client_secret, redirect_uri):
        """
            Create a SpotifyManager object.

            :param username: The Spotify Premium username.
            :param client_id: The client id of your app.
            :param client_secret: The client secret of your app.
            :param redirect_uri: The redirect URI of your app.
        """
        scope = 'playlist-read-private playlist-read-collaborative streaming user-library-read ' \
                'user-library-modify user-read-private user-top-read user-read-playback-state ' \
                'user-modify-playback-state user-read-currently-playing user-read-recently-played'
        token = util.prompt_for_user_token(username, scope, client_id, client_secret, redirect_uri)
        self.sp = Spotify(auth=token)

    # Volume

    def increase_volume(self, volume_percent, device_id=None):
        """
            Increases device's volume in percentage.

            :param volume_percent: Volume percentage to increase. Negative to decrease.
            :param device_id: Device target, if it's not set, target is current device.
            :raises ConnectionError: There is no active device or device_id is not valid.
            :raises TypeError: volume_percent is not an integer.
        """
        if not isinstance(volume_percent, int):
            raise TypeError('volume_percent is not an integer')
        volume = self.get_volume(device_id) + volume_percent
        if volume > 100:
            volume = 100
        elif volume < 0:
            volume = 0
        self.set_volume(volume, device_id)

    def decrease_volume(self, volume_percent, device_id=None):
        """
            Decreases device's volume in percentage.

            :param volume_percent: Volume percentage to decrease. Negative to increase.
            :param device_id: Device target, if it's not set, target is current device.
            :raises ConnectionError: There is no active device or device_id is not valid.
            :raises TypeError: volume_percent is not an integer.
        """
        if not isinstance(volume_percent, int):
            raise TypeError('volume_percent is not an integer')
        self.increase_volume(-volume_percent, device_id)

    def set_volume(self, volume_percent, device_id=None):
        """
            Sets device's volume to new percentage.

            Doesn't throw an error if there is no active device.

            :param volume_percent: Volume percentage to set.
            :param device_id: Device target, if it's not set, target is current device.
            :raises ConnectionError: There is no active device or device_id is not valid.
            :raises TypeError: volume_percent is not an integer.
        """
        if not isinstance(volume_percent, int):
            raise TypeError('volume_percent is not an integer')
        if volume_percent > 100:
            volume_percent = 100
        elif volume_percent < 0:
            volume_percent = 0
        try:
            self.sp.volume(int(volume_percent), device_id)
        except SpotifyException as se:
            if se.http_status == 403:
                raise ConnectionError('There is no active device or device_id is not valid.')
            else:
                raise

    def get_volume(self, device_id=None):
        """
            Returns device's volume in percentage.

            :param device_id: Device target, if it's not set, target is current device.
            :raises ConnectionError: There is no active device or device_id is not valid.
        """
        if device_id:
            dev = self._get_device(device_id)
        else:
            dev = self._get_active_device()
        return dev['volume_percent']

    # Get info

    def get_current_song_info(self):
        """
            Gets information about current song.

            :return: Dictionary.
            :raises ConnectionError: User is not connected to Spotify.
        """
        status = self.sp.currently_playing()
        if not status:
            raise ConnectionError('User not connected to Spotify ')
        return status['item']

    def get_current_album_info(self):
        """
            Gets information about current song's album.

            :return: Dictionary.
            :raises ConnectionError: User is not connected to Spotify.
        """
        return self.get_current_song_info()['album']

    def get_current_song_artist(self):

        """
            Gets artists from current song.

            :return: String of artists names separated by commas.
            :raises ConnectionError: User is not connected to Spotify.
        """
        artists = self.get_current_song_info()['artists']
        artists_string = ''
        for artist in artists:
            artists_string += artist['name'] + ', '
        return artists_string[:-2]

    def get_current_album_release_date(self):

        """
            Gets release year from current song's album.

            :return: Release date as a string with format YYYY-MM-DD.
            :raises ConnectionError: User is not connected to Spotify.
        """
        return self.get_current_song_info()['album']['release_date']

    # Streaming

    def play(self, device_id=None):
        """
            Starts or resumes device's playback.

            Doesn't throw an error if there is no active device.

            :param device_id: Device target, if it's not set, target is current device.
            :raises ConnectionError: There is no active device or device_id is not valid.
        """
        try:
            self.sp.start_playback(device_id)
        except SpotifyException as se:
            if se.http_status == 404:
                raise ConnectionError('There is no active device or device_id is not valid.')
            # Err 403 - Not paused
            elif se.http_status == 403 and 'Forbidden' in se.msg:
                raise ConnectionError('There is no active device or device_id is not valid.')
            else:
                raise

    def pause(self, device_id=None):
        """
            Pauses device's playback.

            Doesn't throw an error if there is no active device.

            :param device_id: Device target, if it's not set, target is current device.
            :raises ConnectionError: There is no active device or device_id is not valid.
        """
        try:
            self.sp.pause_playback(device_id)
        except SpotifyException as se:
            if se.http_status == 404:
                raise ConnectionError('There is no active device or device_id is not valid.')
            # Err 403 - Not paused
            elif se.http_status == 403 and 'Forbidden' in se.msg:
                raise ConnectionError('There is no active device or device_id is not valid.')
            else:
                raise

    def switch_play_pause(self, device_id=None):
        """
            Switch between Play and Pause state.

            Doesn't throw an error if there is no active device.

            :param device_id: Device target, if it's not set, target is current device.
            :raises ConnectionError: There is no active device or device_id is not valid.
        """
        try:
            self.sp.start_playback(device_id)
        except SpotifyException as se:
            # Err 403 - Not paused
            if se.http_status == 403:
                if 'Forbidden' not in se.msg:
                    self.sp.pause_playback(device_id)
                else:
                    raise ConnectionError('There is no active device or device_id is not valid.')
            elif se.http_status == 404:
                raise ConnectionError('There is no active device or device_id is not valid.')
            else:
                raise

    def next_song(self, device_id=None):
        """
            Moves playback to next song.

            Doesn't throw an error if there is no active device.

            :param device_id: Device target, if it's not set, target is current device.
            :raises ConnectionError: There is no active device or device_id is not valid.
        """
        try:
            self.sp.next_track(device_id)
        except SpotifyException as se:
            if se.http_status == 404 or se.http_status == 403:
                raise ConnectionError('There is no active device or device_id is not valid.')
            else:
                raise

    def previous_song(self, restart_time=0, device_id=None):
        """
            Moves playback to previous song. If there is no previous the actual one is restarted.

            If song's peek is greater than restart_time, song is moved instead of restarted.

            Doesn't throw an error if there is no active device.

            :param restart_time: Minimum time in seconds to restart song instead of move playback. 0 to disable.
            :param device_id: Device target, if it's not set, target is current device.
            :raises ConnectionError: There is no active device or device_id is not valid.
            :raises TypeError: volume_percent is not an integer.
        """
        if not isinstance(restart_time, int):
            raise TypeError('restart_time is not an integer')
        if restart_time != 0 and self.sp.currently_playing()['progress_ms']/1000 > restart_time:
                self.restart_song(device_id)
        else:
            try:
                self.sp.previous_track(device_id)
            except SpotifyException as se:
                # Err 403 - No previous track
                if se.http_status == 403:
                    if 'Forbidden' not in se.msg:
                        self.restart_song(device_id)
                    else:
                        raise ConnectionError('There is no active device or device_id is not valid.')
                elif se.http_status == 404:
                    raise ConnectionError('There is no active device or device_id is not valid.')
                else:
                    raise

    def restart_song(self, device_id=None):
        """
            Restarts current song.

            Doesn't throw an error if there is no active device.

            :param device_id: Device target, if it's not set, target is current device.
            :raises ConnectionError: There is no active device or device_id is not valid.
        """
        try:
            self.sp.seek_track(0, device_id)
        except SpotifyException as se:
            if se.http_status == 404 or se.http_status == 403:
                raise ConnectionError('There is no active device or device_id is not valid.')
            else:
                raise

    # Repeat & Shuffle

    def get_repeat_state(self):
        """
            Gets repeat state.

            :return: Repeat state, which can be 'track', 'context' or 'off'.
            :raises ConnectionError: User is not connected to Spotify.
        """
        try:
            return self.sp.current_playback()['repeat_state']
        except TypeError:
            raise ConnectionError('User is not connected to Spotify.')

    def set_repeat_state(self, repeat_state, device_id=None):
        """
            Sets repeat state.

            Doesn't throw an error if there is no active device.

            :param repeat_state: Repeat state, which can be 'track', 'context' or 'off'.
            :param device_id: Device target, if it's not set, target is current device.
            :raises ConnectionError: User is not connected to Spotify.
            :raises TypeError: Repeat state must be 'track', 'context' or 'off'.
        """
        if repeat_state not in ['track', 'context', 'off']:
            raise TypeError('repeat_state must be \'track\', \'context\' or \'off\'.')
        try:
            self.sp.repeat(repeat_state, device_id)
        except SpotifyException as se:
            if se.http_status == 404:
                raise ConnectionError('There is no active device or device_id is not valid.')
            else:
                raise

    def next_repeat_state(self, device_id=None):
        """
            Moves repeat state to next state.

            Order is 'track' -> 'context' -> 'off' -> 'track'.

            :param device_id: Device target, if it's not set, target is current device.
            :raises ConnectionError: User is not connected to Spotify.
        """
        repeat_state = self.get_repeat_state()
        if repeat_state == 'track':
            repeat_state = 'context'
        elif repeat_state == 'context':
            repeat_state = 'off'
        else:
            repeat_state = 'track'
        self.set_repeat_state(repeat_state, device_id)

    def get_shuffle_state(self):
        """
            Gets shuffle state.

            :return: Repeat state, which can be True or False.
            :raises ConnectionError: User is not connected to Spotify.
        """
        try:
            return self.sp.current_playback()['shuffle_state']
        except TypeError:
            raise ConnectionError('User is not connected to Spotify.')

    def set_shuffle_state(self, shuffle_state, device_id=None):
        """
            Sets shuffle state.

            Doesn't throw an error if there is no active device.

            :param shuffle_state: Shuffle state, which can be True or False.
            :param device_id: Device target, if it's not set, target is current device.
            :raises ConnectionError: User is not connected to Spotify.
            :raises TypeError: Shuffle state must be True or False.
        """
        if shuffle_state not in [True, False]:
            raise TypeError('shuffle_state must be True or False.')
        try:
            self.sp.shuffle(shuffle_state, device_id)
        except SpotifyException as se:
            if se.http_status == 404:
                raise ConnectionError('There is no active device or device_id is not valid.')
            else:
                raise

    def switch_shuffle_state(self, device_id=None):
        """
            Switch shuffle state between True and False.

            :param device_id: Device target, if it's not set, target is current device.
            :raises ConnectionError: User is not connected to Spotify.
        """
        self.set_shuffle_state(not self.get_shuffle_state(), device_id)

    # Play

    def play_song(self, song_name, device_id=None):
        """
            Search song that matches song_name and plays it.

            Doesn't throw an error if there is no active device.

            :param song_name: Query to match.
            :param device_id: Device target, if it's not set, target is current device.
            :raises ConnectionError: device_id is not valid.
            :raises TypeError: There is no search query.
            :raises IndexError: There is no results.
        """
        try:
            uri = self.sp.search(song_name, 1, type='track')['tracks']['items'][0]['uri']
            self.sp.start_playback(uris=[uri], device_id=device_id)
        except SpotifyException as se:
            if se.http_status == 400 and 'No search query' in se.msg:
                raise TypeError('There is no search query.')
            elif se.http_status == 404:
                raise ConnectionError('device_id is not valid.')
            else:
                raise
        except IndexError:
            raise IndexError('There is no results.')

    def play_album(self, album_name, device_id=None):
        """
            Search album that matches album_name and plays it.

            Doesn't throw an error if there is no active device.

            :param album_name: Query to match.
            :param device_id: Device target, if it's not set, target is current device.
            :raises ConnectionError: There is no active device or device_id is not valid.
            :raises TypeError: There is no search query.
            :raises IndexError: There is no results.
        """
        try:
            uri = self.sp.search(album_name, 1, type='album')['albums']['items'][0]['uri']
            self.sp.start_playback(context_uri=uri, device_id=device_id)
            self.set_shuffle_state(False, device_id)
        except SpotifyException as se:
            if se.http_status == 400 and 'No search query' in se.msg:
                raise TypeError('There is no search query.')
            elif se.http_status == 404:
                raise ConnectionError('device_id is not valid.')
            else:
                raise
        except IndexError:
            raise IndexError('There is no results.')

    def play_artist(self, artist_name, device_id=None):
        """
            Search artist that matches song_name and plays it.

            Doesn't throw an error if there is no active device.

            :param artist_name: Query to match.
            :param device_id: Device target, if it's not set, target is current device.
            :raises ConnectionError: There is no active device or device_id is not valid.
            :raises TypeError: There is no search query.
            :raises IndexError: There is no results.
        """
        try:
            uri = self.sp.search(artist_name, 1, type='artist')['artists']['items'][0]['uri']
            self.sp.start_playback(context_uri=uri, device_id=device_id)
        except SpotifyException as se:
            if se.http_status == 400 and 'No search query' in se.msg:
                raise TypeError('There is no search query.')
            elif se.http_status == 404:
                raise ConnectionError('device_id is not valid.')
            else:
                raise
        except IndexError:
            raise IndexError('There is no results.')

    def play_genre(self, genre_name, limit=20, device_id=None):
        """
            Search genre that matches genre_name and plays it.

            Doesn't throw an error if there is no active device.

            :param genre_name: Query to match.
            :param limit: Number of songs to search and play.
            :param device_id: Device target, if it's not set, target is current device.
            :raises ConnectionError: There is no active device or device_id is not valid.
            :raises TypeError: genre_name is not valid. Also limit is not an integer.
        """
        if not isinstance(limit, int):
                raise TypeError('limit must be an integer.')
        try:
            results = self.sp.recommendations(seed_genres=[genre_name], limit=limit)['tracks']
            if not results:
                raise TypeError('genre_name must be in ' + str(self.sp.recommendation_genre_seeds()['genres']))
            else:
                uris = []
                for track in results:
                    uris.append(track['uri'])
                self.sp.start_playback(uris=uris, device_id=device_id)
        except SpotifyException as se:
            if se.http_status == 404:
                raise ConnectionError('device_id is not valid.')
            else:
                raise

    def play_playlist(self, playlist_name, device_id=None):
        """
            Search playlist that matches playlist_name and plays it.

            Doesn't throw an error if there is no active device.

            :param playlist_name: Query to match.
            :param device_id: Device target, if it's not set, target is current device.
            :raises ConnectionError: device_id is not valid.
            :raises TypeError: There is no search query.
            :raises IndexError: There is no results.
        """
        try:
            uri = self.sp.search(playlist_name, 1, type='playlist')['playlists']['items'][0]['uri']
            self.sp.start_playback(context_uri=uri, device_id=device_id)
        except SpotifyException as se:
            if se.http_status == 400 and 'No search query' in se.msg:
                raise TypeError('There is no search query.')
            elif se.http_status == 404:
                raise ConnectionError('device_id is not valid.')
            else:
                raise
        except IndexError:
            raise IndexError('There is no results.')

    def play_similar_from_current_artist(self, limit=20, device_id=None):
        """
            Search songs from similar artists of the current one and play them.

            :param limit: Number of songs to search and play.
            :param device_id: Device target, if it's not set, target is current device.
            :raises ConnectionError: There is no active device or device_id is not valid. Also User is
                                     not connected to Spotify.
            :raises TypeError: limit is not an integer.
        """
        if not isinstance(limit, int):
                raise TypeError('limit must be an integer.')
        try:
            artists, uris = [], []
            for artist in self.get_current_song_info()['artists']:
                artists.append(artist['uri'])
            for track in self.sp.recommendations(seed_artists=artists, limit=limit)['tracks']:
                uris.append(track['uri'])
            self.sp.start_playback(uris=uris, device_id=device_id)
        except SpotifyException as se:
            if se.http_status == 404:
                raise ConnectionError('device_id is not valid.')
            else:
                raise

    def play_similar_from_current_track(self, limit=20, device_id=None):
        """
            Search songs similar to the current one and play them.

            :param limit: Number of songs to search and play.
            :param device_id: Device target, if it's not set, target is current device.
            :raises ConnectionError: There is no active device or device_id is not valid. Also User is
                                     not connected to Spotify.
            :raises TypeError: limit is not an integer.
        """
        if not isinstance(limit, int):
            raise TypeError('limit must be an integer.')
        try:
            song_uri = self.get_current_song_info()['uri']
            uris = []
            for track in self.sp.recommendations(seed_tracks=[song_uri], limit=limit)['tracks']:
                uris.append(track['uri'])
            self.sp.start_playback(uris=uris, device_id=device_id)
        except SpotifyException as se:
            if se.http_status == 404:
                raise ConnectionError('device_id is not valid.')
            else:
                raise

    def play_recently_played(self, limit=50, device_id=None):
        """
            Search songs that user played recently.

            :param limit: Number of songs to search and play.
            :param device_id: Device target, if it's not set, target is current device.
            :raises ConnectionError: There is no active device or device_id is not valid. Also User is
                                     not connected to Spotify.
            :raises TypeError: limit is not an integer.
        """
        if not isinstance(limit, int):
            raise TypeError('limit must be an integer.')
        try:
            uris = []
            for track in self.sp.current_user_recently_played(limit)['items']:
                uris.append(track['track']['uri'])
            self.sp.start_playback(uris=uris, device_id=device_id)
        except SpotifyException as se:
            if se.http_status == 404:
                raise ConnectionError('device_id is not valid.')
            else:
                raise

    def play_top_tracks(self, limit=20, device_id=None):
        """
            Search songs that user plays the most and plays them.

            :param limit: Number of songs to search and play.
            :param device_id: Device target, if it's not set, target is current device.
            :raises ConnectionError: There is no active device or device_id is not valid. Also User is
                                     not connected to Spotify.
            :raises TypeError: limit or offset are not an integer.
        """
        if not isinstance(limit, int):
            raise TypeError('limit must be an integer.')
        try:
            uris = []
            for track in self.sp.current_user_top_tracks(limit)['items']:
                uris.append(track['uri'])
            self.sp.start_playback(uris=uris, device_id=device_id)
        except SpotifyException as se:
            if se.http_status == 404:
                raise ConnectionError('device_id is not valid.')
            else:
                raise

    def play_top_artists(self, limit=5, device_id=None):
        """
            Search top songs from artists that user plays the most and plays them.

            :param limit: Number of artists to analyze.
            :param device_id: Device target, if it's not set, target is current device.
            :raises ConnectionError: There is no active device or device_id is not valid. Also User is
                                     not connected to Spotify.
            :raises TypeError: limit or offset are not an integer.
        """
        if not isinstance(limit, int):
            raise TypeError('limit must be an integer.')
        try:
            uris = []
            for artist in self.sp.current_user_top_artists(limit)['items']:
                for track in self.sp.artist_top_tracks(artist['uri'])['tracks']:
                    uris.append(track['uri'])
            self.sp.start_playback(uris=uris, device_id=device_id)
            self.set_shuffle_state(True)
        except SpotifyException as se:
            if se.http_status == 404:
                raise ConnectionError('device_id is not valid.')
            else:
                raise

    # Save & Delete

    def save_current_song(self):
        """
        Saves current song on user's library.

        :raises ConnectionError: User is not connected to Spotify
        """
        self.sp.current_user_saved_tracks_add([self.get_current_song_info()['uri']])

    def delete_current_song(self):
        """
        Deletes current song from user's library.

        :raises ConnectionError: User is not connected to Spotify
        """
        self.sp.current_user_saved_tracks_delete([self.get_current_song_info()['uri']])

    def save_current_album(self):
        """
        Saves current album on user's library.

        :raises ConnectionError: User is not connected to Spotify
        """
        self.sp.current_user_saved_albums_add([self.get_current_album_info()['uri']])

    def delete_current_album(self):
        """
        Saves current album on user's library.

        :raises ConnectionError: User is not connected to Spotify
        """
        uris = []
        for track in self.sp.album_tracks(self.get_current_album_info()['uri'])['items']:
            uris.append(track['uri'])
        self.sp.current_user_saved_tracks_delete(uris)

    def _get_available_devices(self):
        """
            Returns a dict of all the devices available of the current user.

            :return {'devices': [{name, id}, ... ]}
        """
        devices = {'devices': []}
        for dev in self.sp.devices()['devices']:
            devices['devices'].append([dev['name'].capitalize(), dev['id']])
        return devices

    def _get_active_device(self):
        """
            Returns device dict from the active device.

            :return: {id, is_active, is_restricted, name, type, volume_percent}
            :raises ConnectionError: There is no active device.
        """
        for dev in self.sp.devices()['devices']:
            if dev['is_active']:
                return dev
        raise ConnectionError('There is no active device')

    def _get_device(self, device_id):
        """
            Returns device dict from a device ID.

            :param device_id: Device target identifier
            :return: {id, is_active, is_restricted, name, type, volume_percent}
            :raises ConnectionError: There is no active device that match target ID.
        """
        for dev in self.sp.devices()['devices']:
            if dev['id'] == device_id:
                return dev
        raise ConnectionError('There is no active device that match target ID')
