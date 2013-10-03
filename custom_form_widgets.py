from models import db, Status
from wtforms import SelectField

class StatusField(SelectField):
    def __init__(self, *args, **kwargs):
        super(StatusField, self).__init__(*args, **kwargs)
        self.choices = db.session.query(Status.id, Status.status).all()