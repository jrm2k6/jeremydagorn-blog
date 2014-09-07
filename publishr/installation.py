import os
import sys
import csv

class CsvUserDataParser:
    def __init__(self):
        pass

    def parse(self, location_file):
        with open(location_file, 'r+') as handler:
             content = csv.reader(handler)
             for row in content:
                 print ', '.join(row) 
             


def upload_filedata(uploaded_file):
    from base import app
    success = True
    parser = CsvUserDataParser()
    location_to_save = os.getcwd() + '/publishr' + app.config['UPLOAD_FOLDER'] + '/' 
    location_file = location_to_save + uploaded_file.filename 
    try:
        save_file(uploaded_file, location_to_save)
        parser.parse(location_file)
    except ExtensionNotSupportedException as e:
        success = False
    return success


def save_file(_file, destination_folder):
    from base import app
    _filename = _file.filename
    if allowed_file(_filename, app.config['ALLOWED_EXTENSIONS'] or []):
        _file.save(destination_folder + _filename)
    else:
        raise ExtensionNotSupportedException(_filename.split('.')[-1] + 'not in supported extensions')


def allowed_file(_filename, extensions):
    return extensions == set("*") or _filename.split('.')[-1] in extensions


class ExtensionNotSupportedException(Exception):
    pass
