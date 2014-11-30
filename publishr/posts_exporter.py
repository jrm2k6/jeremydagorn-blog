import httplib2
import pprint
import json
import os

from flask import Response
from apiclient.discovery import build
from apiclient.http import MediaFileUpload
from oauth2client.client import OAuth2WebServerFlow, FlowExchangeError


class PostsExporter:
    def __init__(self, client_id, client_secret):
        # Check https://developers.google.com/drive/scopes for all available scopes
        OAUTH_SCOPE = 'https://www.googleapis.com/auth/drive'

        # Redirect URI for installed apps
        REDIRECT_URI = 'urn:ietf:wg:oauth:2.0:oob'

        # Run through the OAuth flow and retrieve credentials
        self.flow = OAuth2WebServerFlow(client_id, client_secret, OAUTH_SCOPE,
                                        redirect_uri=REDIRECT_URI)

    def get_authorize_url(self):
        authorize_url = self.flow.step1_get_authorize_url()
        return authorize_url

    def verify_credentials(self, _code):
        try:
            credentials = self.flow.step2_exchange(_code)
            # Create an httplib2.Http object and authorize it with our credentials
            self.http = httplib2.Http()
            self.http = credentials.authorize(self.http)

            self.exportable_posts = self.get_exportable_posts()
            return Response(json.dumps({'exportablePosts': self.exportable_posts}),
                            status=200, mimetype='application/json')
        except FlowExchangeError:
            return Response(json.dumps({}), status=500, mimetype='application/json')

    def get_exportable_posts(self):
        from base import app
        try:
            directory_to_ls = os.getcwd() + app.config['PATH_POSTS_FOLDER']
            return os.listdir(directory_to_ls)
        except Exception as e:
            return None

    def export_posts(self, selected_posts):
        from base import app
        drive_service = build('drive', 'v2', http=self.http)

        directory_to_ls = os.getcwd() + app.config['PATH_POSTS_FOLDER']
        for post_file in selected_posts:
            media_body = MediaFileUpload(directory_to_ls + post_file, mimetype='text/plain', resumable=True)
            body = {
                'title': post_file,
                'mimeType': 'text/plain'
            }

            exported_file = drive_service.files().insert(body=body, media_body=media_body).execute()
        return Response(json.dumps({}), status=200, mimetype='application/json')
