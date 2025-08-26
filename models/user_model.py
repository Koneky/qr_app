from peewee import Model, CharField, DateTimeField, IntegerField, BooleanField
from datetime import datetime
from data.database import db


class BaseModel(Model):
    class Meta:
        database = db


class User(BaseModel):
    name = CharField(max_length=50)
    full_name = CharField(null=True)
    email = CharField(null=True)
    phone = CharField(null=True)
    avatar_path = CharField(null=True)
    bio = CharField(null=True)
    theme = CharField(default='dark')
    language = CharField(default='ru')
    scan_count = IntegerField(default=0)
    generate_count = IntegerField(default=0)
    history_enabled = BooleanField(default=True)
    is_premium = BooleanField(default=False)
    created_at = DateTimeField(default=datetime.now)
    updated_at = DateTimeField(default=datetime.now)
    last_login = DateTimeField(null=True)
    
    def save(self, *args, **kwargs):
        self.updated_at = datetime.now()
        return super(User, self).save(*args, **kwargs)