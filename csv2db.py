import sqlite3
import csv
import json

def run(file_path, DNAME):
    conn = sqlite3.connect(DBNAME)
    c = conn.cursor()

    c.execute("DROP table if exists 'Laptops'")
    conn.commit()

    c.execute('''CREATE TABLE 'Laptops' (
        'Id'    INTEGER PRIMARY KEY AUTOINCREMENT,
        'SKU'   TEXT NOT NULL, 
        'Model' TEXT,
        'Name'   TEXT,
        'Brand' TEXT,
        'Url'   TEXT,
        'Size'  REAL,
        'Processor Type'    TEXT,
        'Processor' TEXT,
        'Price' REAL,
        'Memory(GB)'    INTEGER,
        'Storage'   TEXT,
        'Color' TEXT,
        'Review Number' INTEGER,
        'Average Rating'   FLOAT   
    );''')
    conn.commit()

    with open(file_path, "r", encoding = "utf-8") as file:
        lines = csv.reader(file, delimiter=',')
        next(lines)
        next(lines)
        for row in lines:
            print(row)
            if (row[13] == "" and int(row[12]) > 0) or row[12] == '3975':
                row[12] = '0'
            if row[0] != "" and row[1] != "":
                row[13] = float(row[13])
                if "tablet" in row[4]:
                    continue
                # Deal with size:
                if float(row[5]) == 0:
                    if "15" in row[4]:
                        row[5] = 15 
                    else:
                        continue
                row[5] = float(row[5])
                # Deal with price:
                if float(row[8]) < 50:
                    continue

                # Deal with storage:
                if row[10] == "16GB Memory":
                    row[9] = 16
                    row[10] = row[11]
                    row[11] = ""
                elif row[10] == "8GB Memory":
                    row[9] = 8
                    row[10] = row[11]
                    row[11] = ""  
                elif row[10] == "4GB Memory":
                    row[9] = 4
                    row[10] = row[11]
                    row[11] = ""
                # Deal with memory:
                if row[9] == "16Gb Memory":
                    row[9] = 16       
                if row[9] == "Tablet":
                    continue  

                if "4gb-memory" in row[4]:
                    row[9] = 4
                elif "8gb-memory" in row[4]:
                    row[9] = 8
                elif "12gb-memory" in row[4]:
                    row[9] = 12
                elif "16gb-memory" in row[4]:
                    row[9] = 16
                elif "32gb-memory" in row[4]:
                    row[9] = 32  
                elif "-2gb-memory" in row[4]:
                    row[9] = 2                    
                else:
                    row[9] = 16              


                # Deal with color:
                if "GB" in row[11]:
                    row[10] = row[11]
                    row[11] = "" 

                # Deal with storage:
                if row[10] == "Pre-Owned" or row[10] == "Preowned" or row[10] == "Pre-owned":
                    if "gb-solid-state-drive" in row[4]:
                        if row[4][(row[4].find("gb-solid-state-drive")-3)].isnumeric() == True:
                            row[10] = row[4][(row[4].find("gb-solid-state-drive")-3):row[4].find("gb-solid-state-drive")] + "GB Solid State Drive"
                        else:
                            row[10] = row[4][(row[4].find("gb-solid-state-drive")-2):row[4].find("gb-solid-state-drive")] + "GB Solid State Drive"
                    if "gb-emmc-flash-memory" in row[4]:
                        row[10] = row[4][(row[4].find("gb-emmc-flash-memory")-2):row[4].find("gb-emmc-flash-memory")] + "GB eMMC Flash Memory"
                    if "gb-ssd" in row[4]:
                        if row[4][(row[4].find("gb-ssd")-3)].isnumeric() == True:
                            row[10] = row[4][(row[4].find("gb-ssd")-3):row[4].find("gb-ssd")] + "GB Solid State Drive"
                        else:
                            row[10] = row[4][(row[4].find("gb-ssd")-2):row[4].find("gb-ssd")] + "GB Solid State Drive"
                    if "gb-hard-drive" in row[4]:
                        if row[4][(row[4].find("gb-hard-drive")-3)].isnumeric() == True:
                            row[10] = row[4][(row[4].find("gb-hard-drive")-3):row[4].find("gb-hard-drive")] + "GB Hard Drive"
                        else:
                            row[10] = row[4][(row[4].find("gb-hard-drive")-2):row[4].find("gb-hard-drive")] + "GB Hard Drive"                                             
                    if "gb-flash-storage" in row[4]:
                        if row[4][(row[4].find("gb-flash-storage")-3)].isnumeric() == True:
                            row[10] = row[4][(row[4].find("gb-flash-storage")-3):row[4].find("gb-flash-storage")] + "GB Flash Storage"
                        else:
                            row[10] = row[4][(row[4].find("gb-flash-storage")-2):row[4].find("gb-flash-storage")] + "GB Flash Storage" 
                elif "Yoga" in row[10]:
                    row[10] = "512 GB SSD"

                row[10] = row[10].replace("SSD","Solid State Drive").strip()
                if int(row[12]) <= 8 and int(row[12]) > 0:
                    row[12] = int(row[12])-1
                insertion = (None, row[1][:-1], row[0][:-1], row[2], row[3], row[4], row[5], row[6], row[7],
                            row[8], (row[9]), row[10], row[11], row[12], row[13])
                statement = "INSERT INTO 'Laptops' VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)"
                c.execute(statement, insertion)

    conn.commit()
    conn.close()


if __name__ == "__main__":
    file_path = "laptop_results.csv"
    DBNAME = 'laptops.db'
    run(file_path, DBNAME)