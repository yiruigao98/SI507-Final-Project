import requests
from bs4 import BeautifulSoup
import json
import sqlite3
import csv

# conn = sqlite3.connect("laptops.db")
# cur = conn.cursor()

# statement = "SELECT t2.[Review 1],t2.[Review 2],t2.[Review 3],t2.[Review 4],t2.[Review 5],t2.[Review 6],t2.[Review 7] FROM Laptops AS t1 JOIN Reviews AS t2 ON t1.SKU=t2.SKU WHERE t1.Id = 1"
# results = cur.execute(statement).fetchone()
# with open('temp_reviews.csv', 'w', newline='') as csvfile:
#     writer = csv.writer(csvfile)
#     for i in results:           
#         writer.writerow([i]) 
# conn.close()


with open("temp_reviews.csv") as f:
    reader = csv.reader(f)
    reviews = [] # reset, start clean
    for r in reader:
        reviews.append(r)
    for review in reviews:
        print(review)