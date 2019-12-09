import requests
from bs4 import BeautifulSoup
import json
import csv

base_url = "https://www.bestbuy.com"
home_url = "https://www.bestbuy.com/site/computers-pcs/laptop-computers/abcat0502000.c?id=abcat0502000"
header = {'User-Agent': 'Mozilla/5.0'}
CACHE_FNAME = 'laptops.json'
# Set up several lists to store key features:
brands = {}
ALLap = []

# Set up a class named Laptop to store the information for each laptop crawled:
class Laptop:
    def __init__(self, name = "", brand = "", url = ""):
        self.name = name
        self.brand = brand
        self.url = url
    
    def update_info(self, size, storage="", processor_type="", processor="", memory=0, color="", price=0, avg_rating = 0, review_num = 0):
        self.size = size
        self.storage = storage
        self.processor_type = processor_type
        self.processor = processor
        self.memory = memory
        self.color = color
        self.price = price
        self.avg_rating = avg_rating
        self.review_num = review_num
        self.reviews = []
    
    def add_reviews(self, review):
        self.reviews.append(review)
        
    def add_tag(self, model, sku):
        self.model = model
        self.sku = sku

    def __str__(self):
        string = "This laptop named %s is of brand %s at link %s. "%(self.name, self.brand, self.url)
        string += "Its model number is %s and the sku number is %s. "%(self.model, self.sku)
        string += "The average rating is %f and the total review number is %d. "%(self.avg_rating, self.review_num)
        string += "The size is %s with processor %s and memory %sGB. "%(str(self.size), self.processor, str(self.memory))
        string += "The storage is %s. "%self.storage
        string += "The color is %s and the price is %s."%(self.color, str(self.price))
        return string


# Caching:
def get_unique_key(url):
    return url

def make_request_using_cache(url, header):
    unique_ident = get_unique_key(url)
    if unique_ident in CACHE_DICTION:
        print("Getting cached data...")
        return CACHE_DICTION[unique_ident]
    else:
        print("Making a request for new data...")
        resp = requests.get(url, headers = header)
        CACHE_DICTION[unique_ident] = resp.text
        dumped_json_cache = json.dumps(CACHE_DICTION)
        fw = open(CACHE_FNAME,"w")
        fw.write(dumped_json_cache)
        fw.close() 
    return CACHE_DICTION[unique_ident]


# Get the information for brands:
def get_brand(page_soup):
    home_soup = page_soup.find_all(class_ = "col-xs-3 flex-panel column")

    for item in home_soup[:11]:
        brand_name = item.find(class_ = "flex-copy-wrapper").text
        brand_url = item.find(class_ = "flex-copy-wrapper").find('a')['href']
        print("This brand named %s has the url as %s"%(brand_name, brand_url))
        brands[brand_name] = brand_url
    
    return brands


# Get the information for laptops of one brand:
def get_product_per_page(brand_soup, product_list):
    product_soup = brand_soup.find_all(class_ = ["sku-item", "appContainer sku-item "])
    for item in product_soup:
        color_set = item.find(class_ = "pl-flex-carousel-slider")
        if color_set == None:
            name = item.find(class_ = "sku-title").text
            url = item.find(class_ = "sku-title").find('a')['href']
            product = Laptop(name, brand_name, url)
            product_list.append(product)
            print("get one!")
        else:
            for color_type in color_set.find_all(class_ = "item"):
                name = color_type.find('a')["data-track"]
                url = color_type.find('a')['href']
                product = Laptop(name, brand_name, url)
                product_list.append(product)   
                print("get one!") 
    return product_list


def get_product(brand_soup, brand_name):
    product_list = []
    next_page_url = ""

    product_list = get_product_per_page(brand_soup, product_list)  
    for a_page in brand_soup.find_all('a'):
        if a_page.text == "Next":
            next_page_url = a_page['href']

    while next_page_url != "":
        print("Find more pages!")
        brand_text = make_request_using_cache(next_page_url, header)
        brand_soup_new = BeautifulSoup(brand_text, 'html.parser')
        product_list = get_product_per_page(brand_soup_new, product_list)
        next_page_url = ""
        for a_page in brand_soup_new.find_all('a'):
            if a_page.text == "Next":
                try:
                    next_page_url = a_page['href']
                except:
                    continue
    return product_list


def get_size(laptop):
    word_para_list = laptop.name.split(' ')
    size = 0
    for word in word_para_list:
        if len(word) > 1:
            if word[-1] == '"':
                size = word[:-1]
                if "." in size:
                    size = float(size)
                elif "." not in size and "," in size:
                    size = float(size.replace(',','.'))
                else:
                    size = int(size)
    return size

def get_mem(memory):
    for word in memory.split(' '):
        if word[-2:] == "GB":
            if len(word) > 2:
                memory = int(word[:-2])
            else:
                memory = int(memory.split(' ')[0])
    return memory
    
def get_info(laptop_soup, laptop):
    # Get hardware parameters:
    name_para_list = laptop.name.split(' - ')
    print(name_para_list)
    
    color = name_para_list[-1]
    storage = name_para_list[-2]
    memory = name_para_list[-3]
    processor_type = ""
    processor = ""
    for para in name_para_list:
        # Judge the type of processors:
        if "Intel" in para:
            processor_type = "Intel"
            processor = para
        elif "AMD" in para:
            processor_type = "AMD"
            processor = para
        elif "MT" in para:
            processor_type = "MediaTek"
            processor = para   
        elif "Snapdragon" in para:
            processor_type = "Snapdragon"
            processor = para               
        elif "Exynos" in para:
            processor_type = "Exynos"
            processor = para    
    # Separate and get desired parameters:
    size = get_size(laptop)
    memory = get_mem(memory)

    # Modify the name:
    name = name_para_list[1]
    laptop.name = name

    # Get price:
    try:
        price = laptop_soup.find(class_ = "priceView-hero-price priceView-customer-price").find(class_ = "sr-only").text.split(' ')[-1][1:]
        price = float(price.replace(',',''))
    except:
        price = 0 

    # Get rating and review number:
    try:
        avg_rating = float(laptop_soup.find(class_ = "c-review-average").text)
    except:
        avg_rating = 0
    try:
        review_num = int(laptop_soup.find(class_ = "c-total-reviews").text.strip().split(' ')[0][1:].replace(',','').replace(')',''))
    except:
        review_num = 0
  
    # Add model and SKU numbers:
    try:
        model = laptop_soup.find_all(class_ = "product-data-value body-copy")[0].text
    except:
        model = ""
    try:
        sku = laptop_soup.find_all(class_ = "product-data-value body-copy")[1].text
    except:
        sku = ""
    laptop.add_tag(model, sku)

    # Update laptop:
    laptop.update_info(size, storage, processor_type, processor, memory, color, price, avg_rating, review_num)

    # Add reviews:
    try:
        for review in laptop_soup.find_all(class_ = "review-item"):
            laptop.add_reviews(eval(review.find('script').text)['reviewBody'])
    except:
        laptop.add_reviews("")


def get_single_review(laptop):
    reviews = []
    while len(laptop.reviews) > 1:
        reviews.append(laptop.reviews.pop(0))
    while len(reviews) < 8:
        reviews.append("")
    return reviews


try:
    cache_file = open(CACHE_FNAME, 'r')
    cache_contents = cache_file.read()
    CACHE_DICTION = json.loads(cache_contents)
    cache_file.close()
except:
    CACHE_DICTION = {}

# The home page:
page_text = make_request_using_cache(home_url, header)
page_soup = BeautifulSoup(page_text, 'html.parser')
brands = get_brand(page_soup)

# Brand page for each brand:
for brand_name in brands.keys():
    if brand_name in ['Intel','AMD','NVIDIA GeForce GTX','Acer','Samsung','ASUS','Lenovo']:
        continue
    print("We are manipulating the products for brand %s"%brand_name)
    brand_url = base_url + brands[brand_name]
    brand_text = make_request_using_cache(brand_url, header)
    brand_soup = BeautifulSoup(brand_text, 'html.parser')
    apple_product = get_product(brand_soup, brand_name)
    print(len(apple_product))
    ALLap.extend(apple_product)
print("The total number of laptops is %d"%len(ALLap))

# Set up a csv file to write data into:
with open('laptop_results.csv','w') as f:
    writer = csv.writer(f)
    writer.writerow(['Model','SKU','Name','Brand','Url','Size','Processor Type','Processor','Price',
                        'Memory(GB)','Storage','Color','Review Numbers','Average Ranking'])

with open('laptop_reviews.csv','w') as f:
    writer = csv.writer(f)
    writer.writerow(['SKU','Review 1','Review 2','Review 3','Review 4','Review 5','Review 6','Review 7','Review 8'])

# Go through all laptops and fetch their information:
for laptop in ALLap:
    print(laptop.name)
    if base_url not in laptop.url:
        laptop.url = base_url + laptop.url
    print(laptop.url)
    laptop_text = make_request_using_cache(laptop.url, header)
    laptop_soup = BeautifulSoup(laptop_text, 'html.parser')
    get_info(laptop_soup, laptop)
    print(str(laptop))
    with open('laptop_results.csv','a', newline = '', encoding = 'utf-8') as f:
        writer = csv.writer(f)
        writer.writerow([laptop.model,laptop.sku,laptop.name,laptop.brand,laptop.url,laptop.size,laptop.processor_type,
                        laptop.processor, laptop.price,laptop.memory,laptop.storage,laptop.color,
                        laptop.review_num,laptop.avg_rating])
    with open('laptop_reviews.csv','a', newline = '', encoding = 'utf-8') as f:
        writer = csv.writer(f)
        reviews = get_single_review(laptop) 
        writer.writerow([laptop.sku,tuple(reviews)])





