# Featureiden ja rental itemien lisäämisen toiminnallisuudet lisätään tänne
import uuid
from random import choice

import faker_commerce
from faker import Faker
from sqlalchemy import text

from categories import get_categories
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



def insert_items():
    with get_db() as _db:

        # Lisätään fakerin jutut
        fake = Faker()
        fake.add_provider(faker_commerce.Provider)

        # Haetaan categoriat categories.py tiedoston funktion avulla
        categories = get_categories(_db)

        _query = "INSERT INTO rental_items(name, description, created_at, serial_number, cateogries_id) VALUES"

        variables = {} # Tyhjä dictionary, jotta sinne voidaa lisätä tavaraa

        for i in range(100):
            _query += f'(:name{i}, :desc{i}, :created_at{i}, :sn{i}, :categories_id{i}),'
            variables[f'name{i}'] = fake.ecommerce_name()
            variables[f'desc{i}'] = fake.text()
            variables[f'created_at{i}'] = fake.date()
            variables[f'sn{i}'] = str(uuid.uuid4()) # Arpoo random merkkijonon
            variables[f'categories_id{i}'] = choice(categories) # choice on randomin toiminto, joka arpoo random järjestyksen.

        _query = _query[:-1]

        # Ajetaan query
        _db.execute(text(_query), variables)

        # Commitoidaan
        _db.commit()