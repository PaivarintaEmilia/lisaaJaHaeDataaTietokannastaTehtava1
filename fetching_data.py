# importit
import mysql.connector
from sqlalchemy import text
from db import get_db


# Funktio, joka hakee kaikki käyttäjätiedot auth_users taulusta --> TÄMÄ ON TESTI
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



# 1. KYSELY

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


# 2. KYSELY

def rental_data_month_daily():
    with get_db() as _db:

        # Kysytään haluttu vuosi käyttäjältä
        while True:
            _year = input("Kerro vuosi:\n")
            if _year.isdigit() and len(_year) == 4:
                break
            else:
                print("Syötä vuosi neljänä numerona.")

        _month = input("Kerro haluttu kuukausi:\n")

        _query = text("SELECT YEAR(created_at) as y, MONTH(created_at) as m, DAY(created_at) as d, COUNT(*) as renteditems "
                      "FROM rental_transactions "
                      "WHERE YEAR(created_at) = :year AND MONTH(created_at) = :month "
                      "GROUP BY DAY(created_at);")


        try:
            results = _db.execute(_query, {'year': _year, 'month': _month})

            answer = [row._asdict() for row in results]

            return answer

        except mysql.connector.Error as err:
            print(f"Virhe suoritettaessa kyselyä: {err.errno}")
            print(f"Virheviesti: {err.msg}")
            _db.rollback()
        else:
            # Suoritetaan vain jos virhettä ei tapahdu
            _db.commit()



# 3. KYSELY

def rental_data_year_monthly():
    with get_db() as _db:

        # Kysytään haluttu vuosi käyttäjältä
        while True:
            _year = input("Kerro vuosi:\n")
            if _year.isdigit() and len(_year) == 4:
                break
            else:
                print("Syötä vuosi neljänä numerona.")



        _query = text("ELECT YEAR(created_at) as y, MONTH(created_at) as m, COUNT(*) as renteditems "
                      "FROM rental_transactions "
                      "WHERE YEAR(created_at) = :year "
                      "GROUP BY MONTH(created_at);")


        try:
            results = _db.execute(_query, {'year': _year})

            answer = [row._asdict() for row in results]

            return answer

        except mysql.connector.Error as err:
            print(f"Virhe suoritettaessa kyselyä: {err.errno}")
            print(f"Virheviesti: {err.msg}")
            _db.rollback()
        else:
            # Suoritetaan vain jos virhettä ei tapahdu
            _db.commit()



# 4. KYSELY

def top_10_most_rented_items():
    with get_db() as _db:


        _query = text("SELECT rental_items.name, COUNT(rental_items.name) AS esiintymiskerrat "
                      "FROM rental_transactions "
                      "INNER JOIN rental_items ON rental_transactions.rental_items_id = rental_items.id "
                      "GROUP BY rental_items.name "
                      "ORDER BY esiintymiskerrat DESC "
                      "LIMIT 10;")



        try:
            results = _db.execute(_query)

            answer = [row._asdict() for row in results]

            #
            return answer

        except mysql.connector.Error as err:
            print(f"Virhe suoritettaessa kyselyä: {err.errno}")
            print(f"Virheviesti: {err.msg}")
            _db.rollback()
        else:
            # Suoritetaan vain jos virhettä ei tapahdu
            _db.commit()



# 5. KYSELY

def top_10_most_rented_items_by_chosen_month():
    with get_db() as _db:


        while True:
            _year = input("Kerro vuosi:\n")
            if _year.isdigit() and len(_year) == 4:
                break
            else:
                print("Syötä vuosi neljänä numerona.")


        _query = text("SELECT rental_items.name, COUNT(rental_items.name) AS esiintymiskerrat, YEAR(rental_transactions.created_at) as y, MONTH(rental_transactions.created_at) as m "
                      "FROM rental_transactions "
                      "INNER JOIN rental_items ON rental_transactions.rental_items_id = rental_items.id "
                      "WHERE YEAR(rental_transactions.created_at) = :year "
                      "GROUP BY y, m, rental_items.name ORDER BY y, m, esiintymiskerrat DESC "
                      "LIMIT 10;")



        try:
            results = _db.execute(_query, {'year': _year})

            answer = [row._asdict() for row in results]

            return answer

        except mysql.connector.Error as err:
            print(f"Virhe suoritettaessa kyselyä: {err.errno}")
            print(f"Virheviesti: {err.msg}")
            _db.rollback()
        else:
            # Suoritetaan vain jos virhettä ei tapahdu
            _db.commit()


# 6. KYSELY

def which_month_has_most_rented_items():
    with get_db() as _db:


        while True:
            _year = input("Kerro vuosi:\n")
            if _year.isdigit() and len(_year) == 4:
                break
            else:
                print("Syötä vuosi neljänä numerona.")


        _query = text("SELECT MONTH(created_at) as m, COUNT(created_at) as lasketutKuukaudet "
                      "FROM rental_items WHERE YEAR(created_at) = :year "
                      "GROUP BY m "
                      "ORDER BY lasketutKuukaudet DESC;")



        try:
            results = _db.execute(_query, {'year': _year})

            answer = [row._asdict() for row in results]

            #
            return answer

        except mysql.connector.Error as err:
            print(f"Virhe suoritettaessa kyselyä: {err.errno}")
            print(f"Virheviesti: {err.msg}")
            _db.rollback()
        else:
            # Suoritetaan vain jos virhettä ei tapahdu
            _db.commit()