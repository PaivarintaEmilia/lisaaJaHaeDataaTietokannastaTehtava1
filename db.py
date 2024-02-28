# TÄÄLLÄ HOIDETAAN TIETOKANTAAN YHDISTÄMISET
import contextlib

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# Tämä jätetään vertailuksi, koska tällä tavalla pitää aina muistaa sulkea yhteys databaseen
def get_db1():
    engine = create_engine('mysql+mysqlconnector://root:@localhost/laplanduas_rental')
    db_session = sessionmaker(bind=engine)
    return db_session()


# Tämä oikea tapa miten tulee suorittaa
@contextlib.contextmanager
def get_db():
    _db = None
    try:
        engine = create_engine('mysql+mysqlconnector://root:@localhost/laplanduas_rental')
        db_session = sessionmaker(bind=engine)
        # Yeld on sama mitä return mutta se ei sulje toimintaa vaan palaa tänne takaisin ja sulkee yhteyden automaattisesti.
        yield _db
    finally:
        if _db is not None:
            # Yhteys katkaistaan täällä eikä users.py
            _db.close()
