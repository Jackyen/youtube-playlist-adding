import os
import google_auth_oauthlib
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from google.oauth2.credentials import Credentials

# Replace with your own playlist ID
playlist_id = 'xxx'

# Replace with the path to your text file containing the list of songs
song_file_path = 'list.txt'

# Authorize the request
creds = ''
if os.path.exists('token.json'):
    creds = Credentials.from_authorized_user_file('token.json', ['https://www.googleapis.com/auth/youtube.force-ssl'])
else:
    flow = google_auth_oauthlib.flow.InstalledAppFlow.from_client_secrets_file('client_secrets.json', ['https://www.googleapis.com/auth/youtube.force-ssl'])
    creds = flow.run_local_server(port=0)
    with open('token.json', 'w') as token:
        token.write(creds.to_json())

youtube = build( 'youtube','v3', credentials=creds)

# Read the list of songs from the file
with open(song_file_path, 'r') as f:
    songs = f.readlines()

# Add each song to the playlist
for song in songs:
    # Search for the video

    search_response = youtube.search().list(
        q=song,
        part='id',
        type='video',
        maxResults=1
    ).execute()

    # Get the video ID from the search results
    video_id = search_response['items'][0]['id']['videoId']

    # Add the video to the playlist
    try:
        request = youtube.playlistItems().insert(
            part='snippet',
            body={
                'snippet': {
                    'playlistId': playlist_id,
                    'resourceId': {
                        'kind': 'youtube#video',
                        'videoId': video_id
                    }
                }
            }
        )
        response = request.execute()
        print(f'The video {video_id} has been added to the playlist {playlist_id}.')
    except HttpError as error:
        print(f'An error occurred: {error}')
        response = None


