import os
import subprocess
import sys

class DatabaseImporter:
    def __init__(self, database_path, uploaded_file):
        self.database_path= database_path
        self.uploaded_file = uploaded_file

    def run(self):
        from base import app
        try:
            location_to_save = os.getcwd() + '/publishr' + app.config['UPLOAD_FOLDER'] + '/'
            destination_uploaded_file = location_to_save + self.uploaded_file.filename
            database_file_path = self.database_path.split("sqlite:///")[1]
            self.uploaded_file.save(destination_uploaded_file)
            command = "cat {0} | sqlite3 {1}".format(destination_uploaded_file, database_file_path)
            subprocess.check_output(command, shell=True)
        except Exception as e:
            print e
