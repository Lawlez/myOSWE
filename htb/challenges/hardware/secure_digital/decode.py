import csv

Data = []
Junk = ["\\0"]

with open("data.csv", 'r', encoding="utf-8") as csvfile:
    file = csv.reader(csvfile)

    for row in file:
        if row[3].isascii():
            Data.append(row[3])
Data.pop(0)

for _ in Junk:
    while _ in Data:
        Data.remove(_)

print("".join(Data))