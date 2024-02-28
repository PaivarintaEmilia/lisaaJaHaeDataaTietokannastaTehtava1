# Lisätään kategorioiden lisäämisen toiminnallisuus tänne
import faker_commerce
from sqlalchemy import text

from db import get_db


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