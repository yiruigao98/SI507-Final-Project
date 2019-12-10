# SI507-final-project
This is the final project for SI 507


## Project Overview

For this project, I focused on laptops sold on BestBuy website. The main intention I want to do is to get the laptop
information from Bestbuy and store it into a well-designed database. My laptop database will provide an interface for users to use
simple commands to search for information that they want to know. I also tried to allow users to compare diﬀerent laptops by
providing visualizations on laptops.

In terms of data, I used Python modules Requests and Beautifulsoup to crawl the data for laptops on BestBuy, especially parameters for each laptop. Due to the storage, I only selected four brands for the laptops, they are Apple, Microsoft Surface, HP and Dell. The crawling task covers pages with different hierarchies and  I needed to do some data analysis for my database including sorting, categorization,
etc. 

Anyone who wants to purchase or know the information of laptops would be one of my targeted populations. I would like my
work, fnally, to simulate an e-commerce website and provide more convenience to users.


## File Details

Since there are a lot of files you can found in this repository, in this section, I will introduce the usage of each file.

First, there is a cache file called **laptops.json** that stores all raw data of laptops. To generate this file, you can use execute **crawl.py** and it will also generate two csv files, one is **laptop_results.csv**, containing the information for each laptop, and the other is **laptop_reviews.csv**, including the reviews on BestBuy for each laptop. These two files are very crucial to build the database.

Execute **csv2db.py** and **review2db.py** will end up with a database with two tables, laptops and reviews, as **laptops.db**. The SKU parameter in the laptops table remains a foreign key with the reviews table. 

The major py file, **interaction.py** procides three major options for users to see the data they filter up. One is to show the data directly in the console, another option is to use plotly to form visualizations in a webpage, the last one is to use Flask and generate webpages. There are several help documents and you will be able to see them all as you execute **interaction.py**.

To be specific, if you choose the Flask option to view the data, you will need to use **interaction.py** to generate csv files that form the filtered data. Then you need to run **source Laptops/Scripts/activate** and **python app.py** to show the html information on webpages. The templates serve for different webpages at different cases.

Additionally, file **proj_test.py** is a unit test file for checking the correctness of the database.

*If you have further question or stuck at how to use a particular file, be free to email me at yiruigao@umich.edu*.
