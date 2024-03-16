# importit
import mysql.connector
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



# Funktio, jolla haetaan lainauksien määrä valitulla kuukaudelta viikoittain
# SELECT YEAR(created_at) as y, MONTH(created_at) as m, COUNT(*) as renteditems FROM rental_transactions WHERE YEAR(created_at) = 2000 AND MONTH(created_at) = 1 GROUP BY WEEK(created_at);
def rental_data_month_week():
    with get_db() as _db:

        # Kysytään haluttu vuosi käyttäjältä
        while True:
            _year = input("Kerro vuosi:\n")
            if _year.isdigit() and len(_year) == 4:
                break
            else:
                print("Syötä vuosi neljänä numerona.")

        # Miten pakotetaan neljä numeroinen syöte??
        _month = input("Kerro haluttu kuukausi:\n")

        _query = text("SELECT YEAR(created_at) as y, MONTH(created_at) as m, COUNT(*) as renteditems "
                      "FROM rental_transactions "
                      "WHERE YEAR(created_at) = :year AND MONTH(created_at) = :month "
                      "GROUP BY WEEK(created_at);")



        # Toinen tapa suorittaa kysely, jos tarvetta

        # _query = text("SELECT YEAR(created_at) as y, MONTH(created_at) as m, COUNT(*) as renteditems "
                     # "FROM rental_transactions "
                     # "WHERE YEAR(created_at) = '%s' AND MONTH(created_at) = '%s' "
                     # "GROUP BY WEEK(created_at);" % (_year, _month))





        try:
            # results = _db.execute(_query)
            results = _db.execute(_query, {'year': _year, 'month': _month})

            # Kerätään kaikki rivit listaksi sanakirjoja
            answer = [row._asdict() for row in results]

            # Palautetaan kaikki käyttäjät
            return answer

        except mysql.connector.Error as err:
            print(f"Virhe suoritettaessa kyselyä: {err.errno}")
            print(f"Virheviesti: {err.msg}")
            _db.rollback()
        else:
            # Suoritetaan vain jos virhettä ei tapahdu
            _db.commit()