import json
import os
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import boto3
from datetime import datetime


def lambda_handler(event, context):
    SPOTIFY_CLIENT_ID = os.environ.get('SPOTIFY_CLIENT_ID')
    SPOTIFY_CLIENT_SECRET = os.environ.get('SPOTIFY_CLIENT_SECRET')

    client_credentials_manager = SpotifyClientCredentials(client_id=SPOTIFY_CLIENT_ID,client_secret=SPOTIFY_CLIENT_SECRET)
    sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)
    playlists = sp.user_playlists('spotify')

    playlist_link = 'https://open.spotify.com/playlist/4hOKQuZbraPDIfaGbM3lKI'
    playlist_URI = playlist_link.split('/')[-1].split('?')[0]

    spotify_data = sp.playlist_tracks(playlist_URI)
    
    client = boto3.client('s3')

    filename = 'spotify_raw_' + str(datetime.now()) + '.json'

    client.put_object(
        Bucket='spotify-etl-project-nimish',
        Key='raw_data/to_processed/'+filename,
        Body=json.dumps(spotify_data)
    )