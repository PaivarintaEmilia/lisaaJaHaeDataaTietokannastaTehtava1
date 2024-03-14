# Featureiden ja rental itemien lisäämisen toiminnallisuudet lisätään tänne
import uuid
from random import choice

import faker_commerce
from faker import Faker
from sqlalchemy import text

from categories import get_categories
from db import get_db
from users import get_users


# Haetaan itemien id:t, jotta ne saadaan randomistsi valittua, kun yhdistellään featureita ja rental_itemeita
def _get_items(_db):
    _query = "SELECT id FROM rental_items"
    ids = []
    rows = _db.execute(text(_query))
    for row in rows:
        ids.append(row[0])
    return ids


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

        _query = "INSERT INTO rental_items(name, description, created_at, serial_number, categories_id) VALUES"

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


# Tämä on apufunktio, jolla saadaan featureiden id:t, jotta voidaan yhdistää featuret ja rental_itemit
# Tämä on sama mitä itemeillä
# Featureita oli color, material, price & size
def _get_features(_db):
    _query = "SELECT id, feature FROM features"
    rows = _db.execute(text(_query))
    _features = []
    for row in rows:
        _features.append({'id': row[0], 'feature': row[1]})
    return _features


# Tehdään seruaavaksi funktio, jossa yhdistellään randomisti rental_itemeitä ja featureita ASETETAANKO VALUET MYÖS??

def mix_features_and_items():
    with get_db() as _db:
        # Käytetään fakeria hinnan arpomiseen
        fake = Faker()
        fake.add_provider(faker_commerce.Provider)

        # Lista värivaihtoehdoista, jotka asetetaan randomisti jos feature on color
        colors = ['black', 'cyan', 'yellow', 'white', 'red', 'pink']

        # Lista kokovaihtoehdoista, jotka asetetaan rondomisti jos feature on size
        sizes = ['XXS', 'XS', 'S', 'M', 'L', 'XL', 'XXL', '3XL']

        items = _get_items(_db) # Eli _get_items funktiolla haetaan kaikki rental_temien id:t
        features = _get_features(_db) # Eli haetaan feature ja sen id
        _query = "INSERT INTO rental_items_has_features(rental_items_id, features_id, value) VALUES(:item_id, :feature_id, :value)"
        # Tehdään yhdistämisiä 100 kertaa loopissa
        for i in range(100):
            # Lisätään try catch, jotta voidaan hylätä duplicaatit
            try:
                item_id = choice(items) # Valitaan joku rental_item tuote randomilla
                # Käydään kaikki featuret läpi ja asetetaan oikeanlaiset valuet jokaiselle featurelle
                for f in features:
                    # Jos f:n feature (ei id) on color niin asetetaan colors listalta joku väri valueksi
                    if f['feature'] == 'color':
                        value = choice(colors)
                    # Jos taas feature on price niin arvotaan valueksi joku hinta fakerinn avulla
                    elif f['feature'] == 'price':
                        value = fake.ecommerce_price(False)
                    # Jos featuer on size niin otetaan randomisti sizes listasta joku koko
                    elif f['feature'] == 'size':
                        value = choice(sizes)
                    elif f['feature'] == 'material':
                        value = choice(faker_commerce.PRODUCT_DATA['material'])
                    # Executetaan query ja asetetaan aervot kyselyn muuttujiin
                    _db.execute(text(_query), {'item_id': item_id, 'feature_id': f['id'], 'value': value})
                    # Commitetaan aina
                    _db.commit()
            except Exception as e:
                print(e)
                _db.rollback


# Lisätään tavaraa rental_transactions tauluun
def rent_items_transactions():
    with get_db() as _db:
        # Otetaan faker käyttöön
        fake = Faker()

        # Haetaan käyttäjät
        users = get_users(_db)
        # Haetaan itemit
        items = _get_items(_db)

        _query = "INSERT INTO rental_transactions(created_at, due_date, auth_users_id, rental_items_id) VALUES"

        # Dictionary
        variables = {}

        for i in range(100):
            _query += f'(:created_at{i}, :due_date{i}, :auth_users_id{i}, :rental_items_id{i}),'
            variables[f'created_at{i}'] = fake.date()
            variables[f'due_date{i}'] = fake.date()
            variables[f'auth_users_id{i}'] = choice(users)
            variables[f'rental_items_id{i}'] = choice(items)

        _query = _query[:-1]

        _db.execute(text(_query), variables)
        _db.commit



