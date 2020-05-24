import requests #http request library in python
import urllib.parse #lets you get and work with a URL

class SpotifyClient(object):
    def __init__(self, api_token):
        self.api_token = api_token  #OAuth token

    def search_song(self, artist, track):
        query = urllib.parse.quote(f'{artist}{track}')  #create string with needed artist + track
        url = f"https://api.spotify.com/v1/search?q={query}&type=track"
        response = requests.get(    #issue get request
            url,
            headers={
             "Content-Type": "application/json",
             "Authorization": f"Bearer {self.api_token}"
            }
        )
        response_json = response.json()
        results = response_json['tracks']['items']  #get tracks from response
        if results:
            return results[0]['id'] #return id of first song result if spotify could find a song that matched youtube song
        else:
            print(f"No song found for {artist} = {track}")



    def add_song_to_spotify(self, song_id):
        url = "https://api.spotify.com/v1/me/tracks"
        response = requests.put(
            url,
            json = {
                "ids": [song_id]    #add one song from array of song ids
            },
            headers = {
                "Content-Type": "application/json",
                "Authorization": f"Bearer {self.api_token}"
            }
        )

        return response.ok  #returns if response was successful or not
