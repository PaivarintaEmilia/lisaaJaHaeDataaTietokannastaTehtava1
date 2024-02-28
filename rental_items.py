# Featureiden ja rental itemien lisäämisen toiminnallisuudet lisätään tänne
from sqlalchemy import text

from db import get_db


def insert_features():
    with get_db() as _db:

        _query = "INSERT INTO features(feature) VALUES(:feature)"

        # Koska featuret keksitään itse, ei tarvita faker juttuja tähän.
        for _feature in ['material', 'size', 'price', 'color']:
            try:
                _db.execute(text(_query), {'feature': _feature})
                _db.commit()
            except Exception as e:
                print(e)
                _db.rollback()