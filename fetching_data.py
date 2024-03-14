# importit

from sqlalchemy import text
from db import get_db

# Tänne lisätään toiminnallisuudet data hakemiseta

# Tehdään testi haku. Haetaan kaikki tiedot auth_usereista

# QUERY: SELECT * FROM `auth_users`

## lUODAAN FUNKTIO

# Funktio, joka hakee kaikki käyttäjätiedot auth_users taulusta
def get_all_users():
    with get_db() as _db:
        # Määritellään SQL-kysely
        _query = text("SELECT * FROM auth_users")

        # Suoritetaan kysely ja tallennetaan tulokset
        results = _db.execute(_query)

        # Kerätään kaikki rivit listaksi sanakirjoja
        users = [row._asdict() for row in results]

        # Palautetaan kaikki käyttäjät
        return users
