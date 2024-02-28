# Tähän luodaan ikilooppi datan lisäämistä varten
import categories
import users

while True:
    _choice = input("Valitse vaihtoehdoista datan lisäämiseen: (1=lisää roolit, 2=lisää käyttäjiä, 3=lisää kategoriat q= lopeta): ")
    if _choice == 'q':
        break
    elif _choice == '1':
        print("Lisätään roolit")
        users.insert_roles()
    elif _choice == '2':
        # Käyttäjä saa päättää monta käyttäjää lisätään.
        num_of_rows = input("Kuinka monta käyttäjää lisätään? (oletus 10): ")
        if num_of_rows == "":
            num_of_rows = 10
        else:
            num_of_rows = int(num_of_rows)
        users.insert_users(num_of_rows)
    elif _choice == 3:
        categories.insert_categories()