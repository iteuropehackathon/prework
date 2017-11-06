# based on https://github.com/youtube/api-samples/blob/master/python/quickstart.py
# Sample Python code for user authorization

import os

import google.oauth2.credentials

from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from google_auth_oauthlib.flow import InstalledAppFlow
from apiclient import discovery

# The CLIENT_SECRETS_FILE variable specifies the name of a file that contains
# the OAuth 2.0 information for this application, including its client_id and
# client_secret.
CLIENT_SECRETS_FILE = "client_secret.json"

# This OAuth 2.0 access scope allows for full read/write access to the
# authenticated user's account and requires requests to use an SSL connection.
SCOPES = ['https://www.googleapis.com/auth/youtube.force-ssl']
API_SERVICE_NAME = 'youtube'
API_VERSION = 'v3'


API_KEY = '<YOUTUBE API KEY> '


def get_authenticated_service_oauth():
    flow = InstalledAppFlow.from_client_secrets_file(CLIENT_SECRETS_FILE, SCOPES)
    credentials = flow.run_console()
    return build(API_SERVICE_NAME, API_VERSION, credentials=credentials)


def get_authenticated_service():
    return discovery.build(API_SERVICE_NAME, API_VERSION, developerKey=API_KEY)

def get_comments(youtube, video_id):
  res = []
  results = youtube.commentThreads().list(
    part="snippet",
    videoId=video_id,
    # channelId=channel_id,
    textFormat="plainText"
  ).execute()
  for item in results["items"]:
    comment = item["snippet"]["topLevelComment"]
    author = comment["snippet"]["authorDisplayName"]
    text = comment["snippet"]["textDisplay"]
    res.append("Comment by %s: %s" % (author, text))
  return res


def youtube_search(youtube, q):
  # Call the search.list method to retrieve results matching the specified
  # query term.
  search_response = youtube.search().list(
    q=q,
    part='id,snippet',
    maxResults=20
  ).execute()

  videos = []
  channels = []
  playlists = []
  comments = []
  # Add each result to the appropriate list, and then display the lists of
  # matching videos, channels, and playlists.
  for search_result in search_response.get('items', []):
    if search_result['id']['kind'] == 'youtube#video':
      videos.append('%s (%s)' % (search_result['snippet']['title'],
                                 search_result['id']['videoId']))
      comments.extend(
          get_comments(youtube, search_result['id']['videoId'])
      )
    elif search_result['id']['kind'] == 'youtube#channel':
      channels.append('%s (%s)' % (search_result['snippet']['title'],
                                   search_result['id']['channelId']))
    elif search_result['id']['kind'] == 'youtube#playlist':
      playlists.append('%s (%s)' % (search_result['snippet']['title'],
                                    search_result['id']['playlistId']))

  print 'Videos:\n', '\n'.join(videos), '\n'
  print 'Channels:\n', '\n'.join(channels), '\n'
  print 'Playlists:\n', '\n'.join(playlists), '\n'
  print 'Comments:', '\n'.join(comments), '\n'
  return videos, channels, playlists, comments


if __name__ == '__main__':
    os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'
    service = get_authenticated_service()
    youtube_search(service, {'q':"Gillette"})
