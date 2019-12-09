import sqlite3
import csv
import json
from ast import literal_eval as make_tuple

def run(file_path, DNAME):
    conn = sqlite3.connect(DBNAME)
    c = conn.cursor()

    c.execute("DROP table if exists 'Reviews'")
    conn.commit()

    c.execute('''CREATE TABLE 'Reviews' ( 
        'SKU'   TEXT NOT NULL, 
        'Review 1' TEXT,
        'Review 2'   TEXT,
        'Review 3' TEXT,
        'Review 4'   TEXT,
        'Review 5'    TEXT,
        'Review 6' TEXT,
        'Review 7'   TEXT,
        FOREIGN KEY(SKU) REFERENCES Laptops (SKU)
    );''')
    conn.commit()

    with open(file_path, "r", encoding = "utf-8") as file:
        lines = csv.reader(file, delimiter=',')
        next(lines)
        next(lines)
        for row in lines:
            insertion = (row[0][:-1], make_tuple(row[1])[0], make_tuple(row[1])[1], make_tuple(row[1])[2], make_tuple(row[1])[3], 
            make_tuple(row[1])[4],make_tuple(row[1])[5],make_tuple(row[1])[6])
            statement = "INSERT INTO 'Reviews' VALUES (?,?,?,?,?,?,?,?)"
            c.execute(statement, insertion)

    conn.commit()
    conn.close()


if __name__ == "__main__":
    file_path = "laptop_reviews.csv"
    DBNAME = 'laptops.db'
    run(file_path, DBNAME)