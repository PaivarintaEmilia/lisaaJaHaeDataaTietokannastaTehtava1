# Lisätään kategorioiden lisäämisen toiminnallisuus tänne
import faker_commerce
from sqlalchemy import text
from faker import Faker # Ei käytetä?
from db import get_db


# Funktio, jotta kategoriat saadaan yhdistettyä rental itemsin lisäämisen queruun
# Tällä siis saadaan kaikki kategoriat
def get_categories(_db):
    _query = "SELECT id FROM categories"
    rows = _db.execute(text(_query))
    ids = [] # Tyhjä lista
    for row in rows:
        ids.append(row[0])
    return ids



# Funktio kategorioiden lisäämiseen
def insert_categories():
    with get_db() as _db:
        _query = "INSERT INTO categories(name) VALUES(:category)"
        for _category in faker_commerce.CATEGORIES:
            try:
                _db.execute(text(_query), {'category': _category})
                _db.commit()
            except Exception as e:
                print(e)
                _db.rollback()