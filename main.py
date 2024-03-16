# Tähän luodaan ikilooppi datan lisäämistä varten
import fetching_data

import categories
import rental_items
import users

while True:
    _choice = input("Valitse vaihtoehdoista datan lisäämiseen:" 
                    "(1=lisää roolit\n "
                    "2=lisää käyttäjiä\n" 
                    "3=lisää kategoriat\n" 
                    "4=lisätään featuret\n" 
                    "5=lisää tuotteet\n" 
                    "6=lisää ominaisuuksia tuotteisiin\n" 
                    "7=lisää tavaraa transactioihin \n" 
                    "8=testi datan haku \n" 
                    "9=Ensimmäinen kysely \n" 
                    "10=Toinen kysely \n" 
                    "11=Kolmas kysely \n" 
                    "12=Neljäs kysely \n" 
                    "13=Viides kysely \n" 
                    "14=Kuuses kysely \n" 
                    "q= lopeta): ")
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
    elif _choice == '3':
        categories.insert_categories()
    elif _choice == '4':
        rental_items.insert_features()
    elif _choice == '5':
        rental_items.insert_items()
    elif _choice == '6':
        rental_items.mix_features_and_items()
    elif _choice == '7':
        rental_items.rent_items_transactions()
    elif _choice == '8':
        # Voit kutsua tätä funktiota ja tulostaa sen tulokset:
        print_answers = fetching_data.get_all_users()
        for user in print_answers:
            print(user)
    elif _choice == '9':
        print_answers = fetching_data.rental_data_month_week()
        for answers in print_answers:
            print(answers)
    elif _choice == '10':
        print_answers = fetching_data.rental_data_month_daily()
        for answers in print_answers:
            print(answers)
    elif _choice == '11':
        print_answers = fetching_data.rental_data_year_monthly()
        for answers in print_answers:
            print(answers)
    elif _choice == '12':
        print_answers = fetching_data.top_10_most_rented_items()
        for answers in print_answers:
            print(answers)
    elif _choice == '13':
        print_answers = fetching_data.top_10_most_rented_items_by_chosen_month()
        for answers in print_answers:
            print(answers)
    elif _choice == '14':
        print_answers = fetching_data.which_month_has_most_rented_items()
        for answers in print_answers:
            print(answers)