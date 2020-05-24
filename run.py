import os

from Spotify import SpotifyClient
from Youtube import YoutubeClient

if __name__ == '__main__':
    run()

def run():
    spotify_client = SpotifyClient(os.getenv('SPOTIFY_AUTH_TOKEN')) #Spotify API key (os.getenv will get key from ur os terminal)
    youtube_client = YoutubeClient('./credentials/client_secret.json')  #get playlists from yt
    playlists = youtube_client.get_playlists()  #store here

    for index, playlist in enumerate(playlists):
        print(f"{index}: {playlist.title}")
    choice = int(input("Enter your choice: "))  #let them pick playlist with a number to make it easy
    chosen_playlist = playlists[choice]
    print(f"You selected {chosen_playlist.title}")

    songs = youtube_client.get_videos_from_playlist(chosen_playlist.id) #try getting as many songs as there are
    print(f"Attempting to add {len(songs)}")

    for song in songs:
       # spotify_token = input("Enter your Spotify token: ")
       # SpotifyClient(spotify_token)
        spotify_song_id =spotify_client.search_song(song.artist, song.track)    #search song on spotify
        if spotify_song_id:
            added_song = spotify_client.add_song_to_spotify(spotify_song_id)    #add song to spotify
            if added_song:
                print(f"Added {song.artist} - {song.track} to your Spotify Liked Songs")


