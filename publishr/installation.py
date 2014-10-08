import os
import sys
import csv

from publishr.models import db, User, Project, Status, Technology, Category


class CsvUserDataParser:
    STRING_TO_MODEL_NAME = {
        "user": User,
        "project": Project,
        "status": Status,
        "technology": Technology,
        "category": Category
        }

    def __init__(self):
        pass

    def parse(self, location_file):
        items = []
        with open(location_file, 'r+') as handler:
            content = csv.reader(handler)
            for row in content:
                if row[0] in CsvUserDataParser.STRING_TO_MODEL_NAME:
                    item = CsvUserDataItem(row[0], row[1:])
                    items.append(item)
        return items


class CsvUserDataItem:
    def __init__(self, type_item, properties):
        self.type_item = type_item
        self.properties = properties

    @property
    def type(self):
        return self.type_item

    @property
    def valid_properties(self):
        return self.properties

    def __str__(self):
        return '<CsvUserDataItem> ' + self.type_item + ' ' + str(self.properties)


def upload_filedata(uploaded_file):
    from base import app
    success = True
    parser = CsvUserDataParser()
    location_to_save = os.getcwd() + '/publishr' + app.config['UPLOAD_FOLDER'] + '/'
    location_file = location_to_save + uploaded_file.filename
    try:
        save_file(uploaded_file, location_to_save)
        items = parser.parse(location_file)
        if len(items) > 0:
            populate_database(items)
        else:
            raise NoItemsGeneratedFromParsingException()
    except ExtensionNotSupportedException as e:
        success = False
    except NonExistentModelException as e:
        success = False
    return success


def populate_database(items):
    for item in items:
        type_item = item.type
        properties = item.properties
        from base import app
        try:
            current_model_name = app.MODELS_NAMES[type_item]
            properties_tuples = zip(current_model_name.get_settable_columns(), properties)
            new_database_item = current_model_name.from_list(properties_tuples)
            db.session.add(new_database_item)
        except KeyError as e:
            db.session.commit()
            raise NonExistentModelException(type_item + ' is not an existing model')
    
    db.session.commit()


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


class NoItemsGeneratedFromParsingException(Exception):
    pass

class NonExistentModelException(Exception):
    pass
