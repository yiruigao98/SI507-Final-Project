#model.py
import csv

BB_FILE_NAME = 'temp_filtered.csv'
CC_FILE_NAME = 'temp_marked.csv'
DD_FILE_NAME = 'temp_reviews.csv'
EE_FILE_NAME = 'temp_compared.csv'

filtered_data = []
marked_data = []
reviews = []
compared_data = []

def init_filter(csv_file_name=BB_FILE_NAME):
    global filtered_data
    with open(csv_file_name) as f:
        reader = csv.reader(f)
        filtered_data = [] # reset, start clean
        for r in reader:
            filtered_data.append(r)

def init_marker(csv_file_name=CC_FILE_NAME):
    global marked_data
    with open(csv_file_name) as f:
        reader = csv.reader(f)
        marked_data = [] # reset, start clean
        for r in reader:
            marked_data.append(r)

def init_reviews(csv_file_name=DD_FILE_NAME):
    global reviews
    with open(csv_file_name) as f:
        reader = csv.reader(f)
        reviews = [] # reset, start clean
        for r in reader:
            reviews.append(r)

def init_comparator(csv_file_name=EE_FILE_NAME):
    global compared_data
    with open(csv_file_name) as f:
        reader = csv.reader(f)
        compared_data = [] # reset, start clean
        for r in reader:
            compared_data.append(r)

def filtered_order(sortby='Id', sortorder='desc'):
    if sortby == 'Id':
        sortcol = 0
    elif sortby == 'Name':
        sortcol = 1
    elif sortby == 'Size':
        sortcol = 3
    elif sortby == "Price":
        sortcol = 5
    elif sortby == "Memory":
        sortcol = 6
    elif sortby == "#Review":
        sortcol = 9
    else:
        sortcol = 10

    rev = (sortorder == 'desc')
    sorted_list = sorted(filtered_data, key=lambda row: row[sortcol], reverse=rev)
    return sorted_list


def marked_order(sortby='Id', sortorder='desc'):
    if sortby == 'Id':
        sortcol = 0
    elif sortby == 'Name':
        sortcol = 1
    elif sortby == 'Size':
        sortcol = 3
    elif sortby == "Price":
        sortcol = 5
    elif sortby == "Memory":
        sortcol = 6
    elif sortby == "#Review":
        sortcol = 9
    else:
        sortcol = 10

    rev = (sortorder == 'desc')
    sorted_list = sorted(marked_data, key=lambda row: row[sortcol], reverse=rev)
    return sorted_list


def get_review():
    return reviews


def compared_order(sortby='Id', sortorder='desc'):
    if sortby == 'Id':
        sortcol = 0
    elif sortby == 'Name':
        sortcol = 1
    elif sortby == 'Size':
        sortcol = 3
    elif sortby == "Price":
        sortcol = 5
    elif sortby == "Memory":
        sortcol = 6
    elif sortby == "#Review":
        sortcol = 9
    else:
        sortcol = 10

    rev = (sortorder == 'desc')
    sorted_list = sorted(compared_data, key=lambda row: row[sortcol], reverse=rev)
    return sorted_list