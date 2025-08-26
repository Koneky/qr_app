from peewee import CharField, IntegerField, BooleanField
from playhouse.migrate import SqliteMigrator, migrate
from data.database import db


def column_exists(table: str, column: str) -> bool:
    rows = db.execute_sql(f"PRAGMA table_info({table});").fetchall()
    return any(r[1] == column for r in rows)

def migrate_user_table():
    migrator = SqliteMigrator(db)
    ops = []

    if not column_exists('user', 'full_name'):
        ops.append(migrator.add_column('user', 'full_name', CharField(null=True)))
    if not column_exists('user', 'bio'):
        ops.append(migrator.add_column('user', 'bio', CharField(null=True)))
    if not column_exists('user', 'scan_count'):
        ops.append(migrator.add_column('user', 'scan_count', IntegerField(default=0)))
    if not column_exists('user', 'generate_count'):
        ops.append(migrator.add_column('user', 'generate_count', IntegerField(default=0)))
    if not column_exists('user', 'histoyry_enabled'):
        ops.append(migrator.add_column('user', 'history_enabled', BooleanField(default=True)))
    if not column_exists('user', 'is_premium'):
        ops.append(migrator.add_column('user', 'is_premium', BooleanField(default=False)))

    if ops:
        migrate(*ops)