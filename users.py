# KÄYTTÄJIEN ROOLIEN LISÄÄMISEN TOIMINNALLISUUDET
import uuid
from random import choice

from faker import Faker
from passlib.context import CryptContext

from db import get_db
from sqlalchemy import text

# Lisätään roolit
def insert_roles():
    # Aloitetaan yhdistämällä tietokantaan
    with get_db() as _db:
        # Kyselyiden tulee aina olla tätä muotoa! Takaa turvallisen syötteen. Muuttujien paikalla aina :muuttujanNimi
        _query = "INSERT INTO roles(role) VALUES(:role)"

        for _role in ['normaluser', 'admin', 'moderator']:
            try:
                # Suoritetaan kysely _query. Muuttuja merkitään tähän (role)
                # Kysely on muotoa ekassa iteraatiossa: INSERT INTO role(role) VALUES('normaluser')
                # Kysely on muotoa tokassa iteraatiossa: INSERT INTO role(role) VALUES('admin') etc..
                _db.execute(text(_query), {'role': _role})
                # Muokkaavat kyselyt tulee commitoida
                _db.commit()

            except Exception as e:
                print(e)
                # Rollback poistaa virheellisen queryn, joka tulee, kun koitetaan syöttää samat kategoriat uudestaan.
                _db.rollback()



# Tehdään apufunktio usersien hakemiselle. Tämä tehdään jotta saadaan usersit rent_items_transactions() funktioon
def get_users(_db):
    _query = "SELECT id FROM auth_users"
    rows = _db.execute(text(_query))
    ids = []
    for row in rows:
        ids.append(row[0])
    return ids


# Apufunktio, jolla haetaan categories, jotta saadaan ne userien lisäämisen yhteydessä.
def _get_roles(_db):
    _query = "SELECT id, role FROM roles"
    rows = _db.execute(text(_query))
    role_ids = [] # Role ids on tyhjä lista
    for row in rows:
        role_ids.append(row[0]) # Row 0 sisältää id:n. Mutta mihin?

    # TUlostaa roolien primary key arvot
    #print(role_ids)
    return role_ids


# Funktio, jolla lisätään käyttäjiä
def insert_users(num_of_rows=10):

    # Tätä käytetään salasanojen kryptaamiseen
    bcrypt_context = CryptContext(schemes=['bcrypt'])

    # Random datan luontiin käytetään fakeria
    fake = Faker()

    with get_db() as _db:
        role_ids = _get_roles(_db)

        variables = {} # Luodaan dictionary

        _query = 'INSERT INTO auth_users(username, password, roles_id) VALUES'
        # Query: INSERT INTO auth_users(username, password, roles_id) VALUES('Emilia', 'salasana(hashattuna)', 'jonkun roolin id')

        for i in range(num_of_rows):
            pwd = bcrypt_context.hash('salasana')
            _random_str = str(uuid.uuid4()) # En ymmärrä mikä on mutta sen takia, että ei tule saman nimisiä käyttäjiä.
            _query += f'(:username{i}, :password{i}, :roles_id{i}),'
            variables[f'username{i}'] = f'{fake.first_name()}-{_random_str}'
            variables[f'password{i}'] = pwd
            variables[f'roles_id{i}'] = choice(role_ids) # choice sen takia, että saadaan randomisti asetettua joku rooli käyttäjälle.

        _query = _query[:-1] # Poistaa viimeisen perästä turhan pilkun

        # Ajetaan query
        _db.execute(text(_query), variables)

        # Muistetaan aina committaa
        _db.commit()