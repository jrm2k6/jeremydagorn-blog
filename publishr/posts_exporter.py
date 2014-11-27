import httplib2
import pprint

from apiclient.discovery import build
from apiclient.http import MediaFileUpload
from oauth2client.client import OAuth2WebServerFlow

class PostsExporter:
    def get_authorize_url(self):
        CLIENT_ID = '147797658892-tfapnr500nqdi16s735i9q745m9719d0.apps.googleusercontent.com'
        CLIENT_SECRET = '26B4YzCxOm88dltPNse9T5vi'

        # Check https://developers.google.com/drive/scopes for all available scopes
        OAUTH_SCOPE = 'https://www.googleapis.com/auth/drive'

        # Redirect URI for installed apps
        REDIRECT_URI = 'urn:ietf:wg:oauth:2.0:oob'

        # Run through the OAuth flow and retrieve credentials
        flow = OAuth2WebServerFlow(CLIENT_ID, CLIENT_SECRET, OAUTH_SCOPE,
                           redirect_uri=REDIRECT_URI)
        authorize_url = flow.step1_get_authorize_url()
        return authorize_url
