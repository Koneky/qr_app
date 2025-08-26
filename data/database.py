import os
from peewee import DatabaseProxy, SqliteDatabase


db = DatabaseProxy()


def init_db(db_path: str):
    # гарантия существования каталога
    os.makedirs(os.path.dirname(db_path), exist_ok=True)

    database = SqliteDatabase(
        db_path,
        pragmas={
            'journal_mode': 'wal',
            'foreign_keys': 1,
            'busy_timeout': 3000
        },
        check_same_thread=False
    )
    db.initialize(database)

    if database.is_closed():
        database.connect(reuse_if_open=True)

def create_tables():
    from models.user_model import User
    from models.history_model import History

    db.create_tables([User, History], safe=True)