# erd_addition_der_natürlichen_Zahlen.py

# neurogames - educational suite
# version 1.0.0

# Vokabeln: addition, summe
# 
# Zone 1 - natürliche Zahlen ohne Null
# größe der Zone wird durch input(manage) bestimmt
# verwendete verwandlungen: +
# verwendete zauberbersprüche: a + b = c
# zwei brocken werden zu einem großen brocken
# zusammen gesdrückt der genau so groß ist wie die Summe der beiden Brocken
# die reihenfolge von a und b ist egal
# standardkonter auf eine erdaddition der natürlichen zahlen ist die
# Start des Hausbaues, links 
## dann richtung rechts vorgehen

## level 1 - zwei brocken werden zu einem großen brocken
## level 2 - drei brocken werden zu einem großen brocken
## level 3 - vier brocken werden zu zwei großen brocken

## eigenen easy bullet log bauen

# am anfang des programms einfach aufrufen:
# log_execution()
# importiere die funktionen aus dem modul

import random

# terminal spiel:
def main():
    level_1()
    #run.level_2()
    #run.level_3()
    print("Glückwunsch du hast alle Level geschafft!")
    time.sleep(2)
    print("Du wirst zum Hauptmenü weitergeleitet")
    time.sleep(2)
    import menu
    menu.main()

def level_1():
    print("Level 1: Zwei Brocken werden zu einem großen Brocken")
    print("Du hast zwei Brocken. Deine Aufgabe ist es, sie zu einem großen Brocken zu verbinden.")
    time.sleep(2)
    range = mana = int(input("Wie groß soll die Zone sein? (z.B. 10): "))
    a = random.randint(1, range)
    b = random.randint(1, range)
    print(f"Deine Brocken sind {a} und {b}.")
    time.sleep(2)
    deine_antwort = int(input("Was ist die Summe der beiden Brocken? "))
    if deine_antwort == a + b:
        print("Richtig! Du hast die Brocken erfolgreich verbunden.")
        time.sleep(2)
        print("Du wirst zum nächsten Level weitergeleitet.")
        print("die richtige Antwort ist:", a + b)
        time.sleep(2)

if __name__ == "__main__":
    import time
    main()
