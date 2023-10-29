from pathlib import Path

import click

from omg.cli import cli
from omg.files.db_updater import DatabaseUpdater
from omg.files.filesystem import FilesystemTagProvider
from omg.files.sqlite import SqliteAudioFileDatabase
from omg.files.walker import FilesystemAudioFileWalker


@cli.group('files')
@click.option('--db')
@click.pass_context
def files(ctx, db):
    ctx.obj['db'] = db


@files.command('update')
@click.argument('path')
@click.pass_context
def update(ctx, path):
    db = SqliteAudioFileDatabase(ctx.obj['db'] or 'omg.sqlite')
    db.init()
    root = Path(path)
    updater = DatabaseUpdater(db, FilesystemTagProvider(root),
                              FilesystemAudioFileWalker(root))
    updater.update()
    pass
