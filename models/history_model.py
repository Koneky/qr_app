from peewee import Model, CharField, DateTimeField
from datetime import datetime
from data.database import db


class BaseModel(Model):
    class Meta:
        database = db


class History(BaseModel):
    created_at = DateTimeField(default=datetime.now)
    type = CharField(null=True)
    data = CharField(null=True)