import httplib2
import pprint
import json
import os
import dropbox

from flask import Response, send_file
from zipfile import ZipFile
from io import BytesIO
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


class PostsExporterArchive(PostsExporter):
    def __init__(self):
        super(PostsExporter, self).__init__()

    def get_response_with_available_files(self):
        self.exportable_posts = self.get_exportable_posts()
        return Response(json.dumps({'exportablePosts': self.exportable_posts}),
                        status=200, mimetype='application/json')

    def export_posts(self, selected_posts):
        memory_file = self.write_zip(selected_posts)
        return send_file(memory_file, attachment_filename='backup.zip', as_attachment=True)

    def write_zip(self, selected_posts):
        from base import app

        directory_to_ls = os.getcwd() + app.config['PATH_POSTS_FOLDER']

        memory_file = BytesIO()
        with ZipFile(memory_file, 'a') as zf:
            for post in selected_posts:
                zf.write(os.path.join(directory_to_ls, post))
        memory_file.seek(0)
        return memory_file


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
            self.credentials = self.flow.step2_exchange(_code)
            # Create an httplib2.Http object and authorize it with our credentials
            _http = httplib2.Http()
            http = self.credentials.authorize(_http)
            self.exportable_posts = self.get_exportable_posts()
            return Response(json.dumps({'exportablePosts': self.exportable_posts}),
                            status=200, mimetype='application/json')
        except FlowExchangeError:
            return Response(json.dumps({}), status=500, mimetype='application/json')

    def export_posts(self, selected_posts):
        from base import app

        # there should be no need to reauthorize - TODO: decorator
        _http = httplib2.Http()
        http = self.credentials.authorize(_http)
        drive_service = build('drive', 'v2', http=http)

        directory_to_ls = os.getcwd() + app.config['PATH_POSTS_FOLDER']

        for post_file in selected_posts:
            media_body = MediaFileUpload(directory_to_ls + post_file, mimetype='text/plain', resumable=True)
            body = {
                'title': post_file,
                'mimeType': 'text/plain'
            }
            exported_file = drive_service.files().insert(body=body, media_body=media_body).execute(http=http)

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
    elif _type == "archive":
        return PostsExporterArchive()

    assert 0, "Bad export type for post exporter creation: " + _type
