from datetime import datetime

from peewee import *

db = SqliteDatabase('jokes.db')


class Joke(Model):
  topic = CharField(max_length=140)
  title = CharField(unique=True, max_length=140)
  content = TextField(unique=True)
  scraped_at = DateTimeField(default=datetime.now)

  class Meta:
    database = db


def add_joke(topic, title, content):
  try:
    Joke.create(topic=topic, title=title, content=content)
  except IntegrityError:
    pass

