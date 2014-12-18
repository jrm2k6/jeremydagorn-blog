import httplib2
import pprint
import json
import os
import dropbox

from flask import Response
from apiclient.discovery import build
from apiclient.http import MediaFileUpload
from oauth2client.client import OAuth2WebServerFlow, FlowExchangeError


class PostsExporter(object):
    def get_exportable_posts(self):
        from base import app
        try:
            directory_to_ls = os.getcwd() + app.config['PATH_POSTS_FOLDER']
            return os.listdir(directory_to_ls)
        except Exception as e:
            return None

class PostsExporterGoogleDrive(PostsExporter):
    def __init__(self, client_id, client_secret):
        # Check https://developers.google.com/drive/scopes for all available scopes
        OAUTH_SCOPE = 'https://www.googleapis.com/auth/drive'

        # Redirect URI for installed apps
        REDIRECT_URI = 'urn:ietf:wg:oauth:2.0:oob'

        super(PostsExporter, self).__init__()
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
            import pdb;pdb.set_trace()
            self.exportable_posts = self.get_exportable_posts()
            return Response(json.dumps({'exportablePosts': self.exportable_posts}),
                            status=200, mimetype='application/json')
        except FlowExchangeError:
            return Response(json.dumps({}), status=500, mimetype='application/json')

    def export_posts(self, selected_posts):
        from base import app

        drive_service = build('drive', 'v2', http=self.http)
        directory_to_ls = os.getcwd() + app.config['PATH_POSTS_FOLDER']
        print directory_to_ls
        for post_file in selected_posts:
            media_body = MediaFileUpload(directory_to_ls + post_file, mimetype='text/plain', resumable=True)
            body = {
                'title': post_file,
                'mimeType': 'text/plain'
            }
            exported_file = drive_service.files().insert(body=body, media_body=media_body).execute(http=self.http)
        return Response(json.dumps({}), status=200, mimetype='application/json')


class PostsExporterDropbox(PostsExporter):
    def __init__(self, client_id, client_secret):
        super(PostsExporter, self).__init__()
        self.flow = dropbox.client.DropboxOAuth2FlowNoRedirect(client_id, client_secret)

    def get_authorize_url(self):
        authorize_url = self.flow.start()
        return authorize_url

    def verify_credentials(self, _code):
        try:
            self.access_token, user_id = self.flow.finish(_code)
            self.exportable_posts = self.get_exportable_posts()
            return Response(json.dumps({'exportablePosts': self.exportable_posts}),
                            status=200, mimetype='application/json')
        except FlowExchangeError:
            return Response(json.dumps({}), status=500, mimetype='application/json')

    def export_posts(self, selected_posts):
        from base import app

        directory_to_ls = os.getcwd() + app.config['PATH_POSTS_FOLDER']
        try:
            client = dropbox.client.DropboxClient(self.access_token)
            for post_file in selected_posts:
                file_name = directory_to_ls + post_file
                f = open(file_name, 'rb')
                response = client.put_file('posts/' + post_file, f)
            return Response(json.dumps({}), status=200, mimetype='application/json')
        except Exception as e:
            return Response(json.dumps({}), status=500, mimetype='application/json')


def post_exporter_factory(_type):
    from base import app

    if _type == "dropbox":
        return PostsExporterDropbox(app.config['DROPBOX_CORE_API_APP_ID'],
                                    app.config['DROPBOX_CORE_API_APP_SECRET'])
    elif _type == "google-drive":
        return PostsExporterGoogleDrive(app.config['GOOGLE_DRIVE_API_CLIENT_ID'], 
                                        app.config['GOOGLE_DRIVE_API_CLIENT_SECRET'])
    assert 0, "Bad export type for post exporter creation: " + _type

