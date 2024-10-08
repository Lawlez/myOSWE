# Variablen und Zuweisung
x = 10  # integer
y = 3.14  # float
name = "Yuki"  # string
is_happy = True  # boolean

# Print gibt keinen Wert zurück, sondern nur die Ausgabe auf der Konsole
print("Das ist ein String", name) #Gibt "Das ist ein String Yuki" auf der Konsole aus

# Input gibt immer einen String zurück
age = input("Gib dein Alter ein: ")#age ist ein String, auch wenn eine Zahl eingegeben wird

# Typkonvertierung
age = int(age)  # Wandelt den String in einen Integer um
height = float(input("Gib deine Größe ein: ")) # Konvertiert den Input direkt zu float
text = str(age) # Wandelt den Integer in einen String um

# Operatoren
# Mathematische Operatoren
a = 5
b = 2
add = a + b  # Addition
sub = a - b  # Subtraktion
mul = a * b  # Multiplikation
div = a / b  # Division (float)
int_div = a // b  # Ganzzahlige Division
mod = a % b  # Modulo (Rest der Division)
exp = a ** b  # Exponentiation

# Vergleichsoperatoren (Geben True oder False zurück)
print(a > b)  # True, weil 5 > 2
print(a < b)  # False, weil 5 nicht kleiner ist als 2
print(a == b)  # False, weil 5 nicht gleich 2 ist
print(a != b)  # True, weil 5 nicht gleich 2 ist
print(x >= 10)  # True, weil 10 >= 10
print(x <= y)   # True, weil 10 <= 20

# Logische Operatoren: and und or
a = True
b = False

print(a and b)  # False, weil einer der Werte False ist
print(a or b)   # True, weil einer der Werte True ist

# Kombinierte Bedingungen
age = 18
has_id = True
# and Beispiel
if age >= 18 and has_id:  # Beide Bedingungen müssen True sein
    print("Du darfst reingehen.")  # Wird ausgegeben

# or Beispiel
is_student = False
is_teacher = True

if is_student or is_teacher:  # Eine der Bedingungen muss True sein
    print("Ermäßigung für den Eintritt.")#Wird ausgegeben, weil is_teacher True ist


# Zuweisungsoperatoren
x = 5
x += 3  # x = x + 3 -> x ist jetzt 8
x -= 2  # x = x - 2 -> x ist jetzt 6
x *= 4  # x = x * 4 -> x ist jetzt 24
x /= 3  # x = x / 3 -> x ist jetzt 8.0

# Identitätsoperatoren
a = 5
b = 5
print(a is b)  # True, weil beide Variablen auf das gleiche Objekt zeigen
print(a is not b)  # False, weil a und b das gleiche Objekt sind

# Mitgliedschaftsoperatoren
name = "Yuki"
print('Y' in name)  # True, weil 'Y' in "Yuki" vorkommt
print('x' not in name)  # True, weil 'x' nicht in "Yuki" vorkommt

# Flow Control (if, elif, else)
x = 15
if x < 10:
    print("x ist kleiner als 10")
elif x < 20:
    print("x ist kleiner als 20 aber größer oder gleich 10")
else:
    print("x ist 20 oder größer")

# Unterschied zwischen if, elif, else und mehreren ifs
x = 10

# Variante mit elif:
if x < 10:
    print("Kleiner als 10")
elif x < 20:
    print("Kleiner als 20")
else:
    print("Größer oder gleich 20")

# Variante mit mehreren ifs (alle if-Blöcke werden überprüft):
if x < 10:
    print("Kleiner als 10")
if x < 20:  # Auch wenn der erste Vergleich false war, wird dieser getestet
    print("Kleiner als 20")
if x >= 20:
    print("Größer oder gleich 20")

# Loops
# while-Schleife (läuft so lange, wie die Bedingung True ist)
i = 0
while i < 5:
    print(i)
    i += 1  # i wird um 1 erhöht

# for-Schleife (läuft über eine Sequenz, z.B. eine Liste oder ein Range)
for i in range(5):  # range(5) gibt die Werte 0, 1, 2, 3, 4
    print(i)

# Funktionen
def greet(name):
    """
    Eine einfache Funktion, die eine Begrüßung ausgibt.
    """
    print("Hallo, " + name)

greet("Yuki")  # Aufruf der Funktion, Ausgabe: "Hallo, Yuki"

# Funktionen können auch Werte zurückgeben
def add_numbers(a, b):
    return a + b

result = add_numbers(5, 3)  # Speichert 8 in result
print(result)  # Ausgabe: 8

# Ohne explizites return gibt eine Funktion None zurück
def no_return():
    print("Ich gebe keinen Wert zurück")

output = no_return()  # output ist None
print(output)  # Ausgabe: None

# Listen (mutable Datenstruktur) (mutierbar=veränderbar)
my_list = [1, 2, 3, 4, 5]
print(my_list[0])  # Zugriff auf das erste Element (1)
len(my_list)    # Gibt die Anzahl elemente in der Lsite zurück (die Länge)

my_list.append(6)  # Fügt ein Element am Ende der Liste hinzu
print(my_list)  # Ausgabe: [1, 2, 3, 4, 5, 6]

my_list.remove(2)  # Entfernt das Element 2 aus der Liste
print(my_list)  # Ausgabe: [1, 3, 4, 5, 6]

# Tuples (immutable Datenstruktur) = unveränderbar
my_tuple = (1, 2, 3, 4, 5)
print(my_tuple[0])  # Zugriff auf das erste Element (1)

# Tuples können nicht geändert werden (führt zu einem Fehler):
#my_tuple[0] = 10 -> TypeError: 'tuple' object does not support item assignment

# Dictionaries (Schlüssel-Wert-Paare)
my_dict = {
    "name": "Yuki",
    "age": 4,
    "breed": "Wolfsspitz"
}

# Zugriff auf Werte über den Schlüssel
print(my_dict["name"])  # Ausgabe: Yuki
print(my_dict["age"])   # Ausgabe: 4

# Hinzufügen eines neuen Schlüssel-Wert-Paars
my_dict["color"] = "gray"
print(my_dict)#Ausgabe: {'name': 'Yuki', 'age': 4, 'breed': 'Wolfsspitz', 'color': 'gray'}

# Entfernen eines Schlüssel-Wert-Paars
del my_dict["breed"]
print(my_dict) #Ausgabe: {'name': 'Yuki', 'age': 4, 'color': 'gray'}

# Objekte (Klassen und Instanzen)
class Dog:
    def __init__(self, name, age):
        self.name = name  # Instanzvariable
        self.age = age

    def bark(self):
        print(self.name + " bellt!")

# Instanziierung eines Objekts
my_dog = Dog("Yuki", 4)  
print(my_dog.name)  # Zugriff auf Attribut, Ausgabe: Yuki
my_dog.bark()  # Aufruf der Methode, Ausgabe: Yuki bellt!
