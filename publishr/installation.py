import os
import sys


class CsvUserDataParser:
    def __init__(self, _path_file):
        self.path_file = _path_file

    def parse(self):
        return ''


def upload_filedata(uploaded_file):
    success = True
    parser = CsvUserDataParser('')
    try:
        save_file(uploaded_file)
    except ExtensionNotSupportedException as e:
        success = False
    return success


def save_file(_file):
    from base import app
    _filename = _file.filename
    if allowed_file(_filename, app.config['ALLOWED_EXTENSIONS'] or []):
        destination_folder = os.getcwd() + '/publishr' + app.config['UPLOAD_FOLDER']
        destination = os.path.join(destination_folder, _filename)
        _file.save(destination)
    else:
        raise ExtensionNotSupportedException(_filename.split('.')[-1] + 'not in supported extensions')


def allowed_file(_filename, extensions):
    return extensions == set("*") or _filename.split('.')[-1] in extensions


class ExtensionNotSupportedException(Exception):
    pass
