import os
import subprocess
import sys


class DatabaseExporter:
    def __init__(self, database_uri):
        self.path_database_file = self.get_path_from_uri(database_uri)

    def run(self):
        from base import app
        try:
            destination_folder = app.config['EXPORTS_FOLDER']
        except KeyError:
            destination_folder = os.path.join(app.config['BASEDIR'], 'exports')

        exported_name = self.path_database_file.split('/')[-1].split('.')[0]
        destination = os.path.join(destination_folder, exported_name)

        if not os.path.exists(destination_folder):
            os.makedirs(destination_folder)

        with open(destination + '.temp', 'w+') as temp_file:
                subprocess.call(["sqlite3", self.path_database_file, ".dump"], stdout=temp_file)

        with open(destination + '.dump', 'w+') as output_file:
                subprocess.call(["grep", "INSERT INTO", destination + '.temp'], stdout=output_file)

        os.remove(destination + '.temp')

    def get_path_from_uri(self, database_uri):
        split_str = database_uri.split("sqlite:///")
        if len(split_str) > 1:
            return split_str[1]
        else:
            raise NoDatabasePathFoundException()


class NoDatabasePathFoundException(Exception):
    pass
