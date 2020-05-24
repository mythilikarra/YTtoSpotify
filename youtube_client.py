import os
import google_auth_oauthlib.flow
import googleapiclient.discovery
import youtube_dl

class Song(object): #to simplify some later steps
    def __init__(self, artist, track):
        self.artist = artist
        self.track = track

class Playlist(object):
    def __init__(self, id, title):
        self.id = id
        self.title = title



class YoutubeClient(object):
    def __init__(self, credentials_location): #constructor
        scopes = ["https://www.googleapis.com/auth/youtube.readonly"]

            # Disable OAuthlib's HTTPS verification when running locally.
            # *DO NOT* leave this option enabled in production.
        os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"

        api_service_name = "youtube"
        api_version = "v3"
           # client_secrets_file = "YOUR_CLIENT_SECRET_FILE.json"

            # Get credentials and create an API client
        flow = google_auth_oauthlib.flow.InstalledAppFlow.from_client_secrets_file(
            credentials_location, scopes)
        credentials = flow.run_console()
        youtube_client = googleapiclient.discovery.build(
            api_service_name, api_version, credentials=credentials)

        self.youtube_client = youtube_client
#above from Youtube Data API

    def get_playlists(self):    #from youtube
        request = self.youtube_client.playlists().list( #function that youtube api has that gets all the playlists
            part="id, snippet", #specify what data you want from the playlist
            maxResults = 50,    #max of 50 playlists
            mine = True         #get our own playlists, not someone else's
        )
        response = request.execute()    #execute the snippet above
        playlists = [Playlist(item['id'], item['snippet']['title']) for item in response['items']]    #response will return a lot of info, here we return playlists as a list

        return playlists

    def get_videos_from_playlist(self, playlist_id):
        songs = []  #array of youtube songs
        request = self.youtube_client.playlistItems().list( #function that gets videos from playlist
            playlistId = playlist_id,
            part="id, snippet",
            maxResults = 50
        )
        response = request.execute()  # execute the snippet above

        for item in response['items']:
            video_id = item['snippet']['resourceId']['videoId'] #get video id data
            artist, track = self.get_artist_and_track_from_video(video_id)  #from youtube dl library since youtube api doesnt get artist and track for you
            if artist and track:    #if an artist and track exist, add to songs dictionary
                songs.append(Song(artist, track))
        return songs
    def get_artist_and_track_from_video(self, video_id):    #use dl library
        youtube_url = f"https.youtube.com/watch?v={video_id}"
        video = youtube_dl.YoutubeDL({'quiet': True}).extract_info( #avoid output logs with quiet = true
            youtube_url, download = False   #dont want to download yt video
        )
        artist = video['artist']
        track = video['track']  #getting artist and track from video

        return artist, track
