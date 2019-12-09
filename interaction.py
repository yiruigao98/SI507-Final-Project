import sqlite3
import csv
import re
import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from pyfiglet import Figlet
from colored import colored, fg, bg, attr
from prettytable import PrettyTable


DBNAME = "laptops.db"

def load_help_text(file_path):
    with open(file_path, encoding='utf-8') as f:
        return f.read()

def process_command(command, marked_id, option):
    conn = sqlite3.connect(DBNAME)
    cur = conn.cursor()

    # Check if there are multiple searching:
    item_dic = {}
    if command.find('|') != -1:
        try:
            command_list = command.split('|')
            for c in command_list:
                try:
                    ope = c.split(':')
                    item_dic[ope[0]] = ope[1]
                except:
                    print("Invalid command!")
        except:
            print("Invalid command!")
    else:
        try:
            ope = command.split(':')
            item_dic[ope[0]] = ope[1]
        except:
            print("Invalid command!")  

    # Print a leading welcome remark!
    print ("%s%s Thanks for choosing!!! %s\n" % (fg('white'), bg('cornflower_blue'), attr('reset')))
    print(load_help_text('detail_help.txt'))
    
    # Search by details:
    sort_ls = input("Please choose how you would like to observe the data, or you can input 'exit' to quit: ")
    while sort_ls != "exit":
        # Default value:
        sortby = "Price"
        order = "top"
        number = 5
        if sort_ls.find('|') != -1:
            sort = sort_ls.split('|')[0]
            ls = sort_ls.split('|')[1]
            if sort.split('=')[0] == "sort" and (ls.split('=')[0] == "top" or ls.split('=')[0] == "bottom"):
                try:
                    sortby = sort.split('=')[1]
                    order = ls.split('=')[0]
                    number = int(ls.split('=')[1])
                except:
                    print("Invalid command!")
            else:
                print("Invalid command!")
        elif sort_ls != '':
            if sort_ls.find('sort') != -1:
                try:
                    sortby = sort_ls.split('=')[1]
                except:
                    print("Invalid command!")
            if sort_ls.find('top') != -1 or sort_ls.find('bottom') != -1:
                try:
                    order = sort_ls.split('=')[0]
                    number = int(sort_ls.split('=')[1])
                except:
                    print("Invalid command!")

        # Form a sql statement to execute the searching:
        key_list = ["brand","price","memory","storage","processor","rating","color","size"]
        base_statement = "SELECT Id,[Name],Brand,Size,Processor,Price,[Memory(GB)],Storage,Color,[Review Number],[Average Rating] FROM Laptops WHERE "
        statement = base_statement
        for item in item_dic.items():
            if item[0] != list(item_dic.keys())[0]:
                statement += "AND "
            if item[0] not in key_list:
                print("Invalid command!")
                return
            # Different categories:
            if item[0] == "brand":
                name = item[1]
                statement += "Brand = '%s' "%name
            elif item[0] == "price":
                min_price = float(item[1].split(' ')[0])
                max_price = float(item[1].split(' ')[1])
                statement += "Price >= %f AND Price <= %f "%(min_price, max_price)
            elif item[0] == "memory":
                value = int(item[1])
                statement += "[Memory(GB)] = %d "%value
            elif item[0] == "storage":
                des = item[1]
                statement += "Storage LIKE '%{des}%' ".format(des=des)
            elif item[0] == "processor":
                name = item[1]
                statement += "Processor LIKE '%{name}%' ".format(name=name)
            elif item[0] == "rating":
                min_rating = float(item[1].split(' ')[0])
                max_rating = float(item[1].split(' ')[1])
                statement += "[Average Rating] >= %f AND [Average Rating] <= %f "%(min_rating, max_rating)
            elif item[0] == "color":
                color = item[1]
                statement += "Color LIKE '%{color}%' ".format(color=color)       
            else:
                if item[1].find(' ') != -1:
                    min_size = float(item[1].split(' ')[0])
                    max_size = float(item[1].split(' ')[1])
                    statement += "Size >= %f AND Size <= %f "%(min_size, max_size)
                else:
                    size = item[1]
                    statement += "Size = %f "%size

        if order == "top":
            statement += "ORDER BY %s DESC "%sortby
        else:
            statement += "ORDER BY %s "%sortby
        statement += "LIMIT %d"%number
        # Execute the sql statement:
        try:
            results = cur.execute(statement)
            print_out_results = results.fetchall()
            # Print out words if no search results:
            print ("%s%s Generating your data table... %s" % (fg('white'), bg('cornflower_blue'), attr('reset')))
            if len(print_out_results) == 0:
                print("\nIt seems no searching results found... What about trying another one?\n")
            # Print filtered data:
            if option == "1":
                x = PrettyTable()
                x.field_names = ["Id", "Name", "Brand", "Size","Processor","Price","Memory","Storage","Color","#Review","Avg. Rating"]
                for row in print_out_results:
                    x.add_row(list(row))
                print(x)
            elif option == "2":
                trace = go.Table(
                    header=dict(
                        values=["Id", "Name", "Brand", "Size","Processor","Price","Memory","Storage","Color","#Review","Avg. Rating"],
                        line_color='darkslategray',
                        fill_color='royalblue',
                        font=dict(color='white', size=20),
                        align="center"
                    ),
                    cells=dict(
                        values=pd.DataFrame.from_records(data = print_out_results).T, 
                        line_color='darkslategray',
                        font = dict(color = 'darkslategray', size = 15),
                        align = "center"
                    )
                )
                layout = dict(autosize=True)
                fig = go.Figure(data = [trace], layout = layout)
                fig.update_layout(
                    showlegend = False,
                    title_text = "This is your filtered data:",
                )
                fig.write_html('filtered.html', auto_open = True)
            elif option == "3":
                with open('temp_filtered.csv', 'w', newline='') as csvfile:
                    writer = csv.writer(csvfile, delimiter=',')
                    for i in range(len(print_out_results)):
                        writer.writerow(list(print_out_results[i]))
            
        except:
            print ("%s%s There's problem with your execution, go and check your execution statement:  %s" % (fg('white'), bg('cornflower_blue'), attr('reset')))
            print(statement)
        
        print("\n")

        print(load_help_text('mark_help.txt'))
        marked = input("Do you want to marked any product (Input the id): ")
        if marked != "" and re.match(r'^[0-9 ]*$', marked):
            if marked.find(' ') != -1:
                for number in marked.split(' '):
                    marked_id.append(int(number))
            else:
                marked_id.append(int(marked))
            marked_id = list(set(marked_id))
        elif marked != "" and re.match(r'^[0-9 ]*$', marked):
            print("This is not an id!")
        
        sort_ls = input("\nPlease choose how you would like to observe the data, or you can input 'exit' to quit: ")

    conn.close()
    return marked_id



def marked_command(marked_id, option):
    conn = sqlite3.connect(DBNAME)
    cur = conn.cursor()
    print ("%s%s Welcome to your marked cart! %s" % (fg('white'), bg('cornflower_blue'), attr('reset')))
    print(load_help_text('mark_help2.txt'))
    command = input("Input your choice: ")
    while command != "leave marked":
        if command == "marked check":

            if option == "1":
                x = PrettyTable()
                x.field_names = ["Id", "Name", "Brand", "Size","Processor","Price","Memory","Storage","Color","#Review","Avg. Rating"]

                for id_ in marked_id:
                    statement = "SELECT Id,[Name],Brand,Size,Processor,Price,[Memory(GB)],Storage,Color,[Review Number],[Average Rating] FROM Laptops WHERE Id = %d"%id_
                    result = cur.execute(statement).fetchone()
                    x.add_row(list(result))
                print(x)

            elif option == "2":
                statement = "SELECT Id,[Name],Brand,Size,Processor,Price,[Memory(GB)],Storage,Color,[Review Number],[Average Rating] FROM Laptops WHERE Id IN ({seq})".format(seq = ','.join('?'*len(marked_id)))
                print_out_results = cur.execute(statement, marked_id).fetchall()

                trace = go.Table(
                    header=dict(
                        values=["Id", "Name", "Brand", "Size","Processor","Price","Memory","Storage","Color","#Review","Avg. Rating"],
                        line_color='darkslategray',
                        fill_color='paleturquoise',
                        font=dict(color='black', size=20),
                        align="center"
                    ),
                    cells=dict(
                        values=pd.DataFrame.from_records(data = print_out_results).T, 
                        fill_color='lavender',
                        font = dict(color = 'darkslategray', size = 15),
                        align = "center"
                    )
                )
                layout = dict(autosize=True)
                fig = go.Figure(data = [trace], layout = layout)
                fig.update_layout(
                    showlegend=False,
                    title_text="These are your marked laptops:",
                )
                fig.write_html('marked.html', auto_open = True)  

            elif option == "3":
                statement = "SELECT Id,[Name],Brand,Size,Processor,Price,[Memory(GB)],Storage,Color,[Review Number],[Average Rating] FROM Laptops WHERE Id IN ({seq})".format(seq = ','.join('?'*len(marked_id)))
                print_out_results = cur.execute(statement, marked_id).fetchall()
                with open('temp_marked.csv', 'w', newline='') as csvfile:
                    writer = csv.writer(csvfile, delimiter=',')
                    for i in range(len(print_out_results)):
                        writer.writerow(list(print_out_results[i]))                

        elif command.find("marked delete") != -1:
            delete_id = int(command[(command.find("marked delete")+14):])
            for id_ in marked_id:
                if id_ == delete_id:
                    marked_id.remove(delete_id)
                    break
            marked_id = list(set(marked_id))
            print("Laptop of Id %d has been deleted!"%delete_id)
        
        elif command.find("marked reviews") != -1:
            print ("%s%s Reviews:  %s" % (fg('white'), bg('cornflower_blue'), attr('reset')))
            review_id = int(command[(command.find("marked reviews")+15):])
            statement = "SELECT t2.[Review 1],t2.[Review 2],t2.[Review 3],t2.[Review 4],t2.[Review 5],t2.[Review 6],t2.[Review 7] FROM Laptops AS t1 JOIN Reviews AS t2 ON t1.SKU=t2.SKU WHERE t1.Id = %d"%review_id
            results = cur.execute(statement).fetchone()
            if option == "1":
                i = 1
                for review in results:
                    if review != "":
                        print("%d.%s"%(i,review))
                        print('\n\n')
                        i += 1
            elif option == "2":
                df = pd.DataFrame(columns=["Reviews"])
                for result in results:
                    df.loc[len(df)] = result

                trace = go.Table(
                    header=dict(
                        values=["Reviews"],
                        line_color='lightgrey',
                        fill_color='paleturquoise',
                        font=dict(color='white', size=20),
                        align="center"
                    ),
                    cells=dict(
                        values=df.T, 
                        fill_color='lavender',
                        font = dict(color = 'darkslategray', size = 15),
                        align = "center"
                    )
                )
                fig = go.Figure(data = [trace])
                fig.update_layout(
                    showlegend=False,
                    title_text="Look at the reviews:",
                )
                fig.write_html('reviews.html', auto_open = True)
            elif option == "3":
                with open('temp_reviews.csv', 'w', newline='') as csvfile:
                    writer = csv.writer(csvfile)
                    for i in results:           
                        writer.writerow([i]) 

            print('\n')
        
        elif command.find("marked compare") != -1:
            id1 = int(command.split(' ')[2])
            id2 = int(command.split(' ')[3])
            if option == "1":
                x = PrettyTable()
                x.field_names = ["Id", "Name", "Brand", "Size","Processor","Price","Memory","Storage","Color","#Review","Avg. Rating"]
                
                statement = "SELECT Id,[Name],Brand,Size,Processor,Price,[Memory(GB)],Storage,Color,[Review Number],[Average Rating] FROM Laptops WHERE Id = %d"%id1
                result = cur.execute(statement).fetchone()
                x.add_row(list(result))
                statement = "SELECT Id,[Name],Brand,Size,Processor,Price,[Memory(GB)],Storage,Color,[Review Number],[Average Rating] FROM Laptops WHERE Id = %d"%id2
                result = cur.execute(statement).fetchone()
                x.add_row(list(result))

                print(x)
            elif option == "2":
                columns =["Id", "Name", "Brand", "Size","Processor","Price","Memory","Storage","Color","#Review","Avg. Rating"]
                df = pd.DataFrame(columns=columns)

                statement = "SELECT Id,[Name],Brand,Size,Processor,Price,[Memory(GB)],Storage,Color,[Review Number],[Average Rating] FROM Laptops WHERE Id = %d"%id1
                result1 = list(cur.execute(statement).fetchone())
                statement = "SELECT Id,[Name],Brand,Size,Processor,Price,[Memory(GB)],Storage,Color,[Review Number],[Average Rating] FROM Laptops WHERE Id = %d"%id2
                result2 = list(cur.execute(statement).fetchone())
                df.loc[0] = result1
                df.loc[1] = result2 

                fig = make_subplots(rows=2, cols=4,
                    specs=[[{"type": "table","colspan": 4},None,None,None],
                        [{"type": "pie"},{"type": "pie"},{"type": "pie"},{"type": "pie"}]],
                    subplot_titles=("Record Table","Price Comparison","Size Comparison","Memory Comparison","Average Rating Comparison")
                )

                fig.add_trace(
                    go.Table(
                        header=dict(
                            values=["Id", "Name", "Brand", "Size","Processor","Price","Memory","Storage","Color","#Review","Avg. Rating"],
                            line_color='darkslategray',
                            fill_color='paleturquoise',
                            font=dict(color='black', size=20),
                            align="center"
                        ),
                        cells=dict(
                            values = df.T, 
                            fill_color='lavender',
                            font = dict(color = 'darkslategray', size = 15),
                            align = "center",
                            height=30
                        )
                    ),
                    row=1, col=1
                )
                fig.add_trace(
                    go.Pie(
                        labels = ['%d'%id1,'%d'%id2],
                        values = [df.loc[0, "Price"], df.loc[1, "Price"]],
                        hole=.3,
                        hoverinfo = 'label',
                        textinfo='value', 
                        textfont_size=20,
                    ),
                    row=2, col=1
                )
                fig.add_trace(
                    go.Pie(
                        labels = ['%d'%id1,'%d'%id2],
                        values = [df.loc[0, "Size"], df.loc[1, "Size"]],
                        hole=.3,
                        hoverinfo = 'label',
                        textinfo='value', 
                        textfont_size=20,
                    ),
                    row=2, col=2
                )
                fig.add_trace(
                    go.Pie(
                        labels = ['%d'%id1,'%d'%id2],
                        values = [df.loc[0, "Memory"], df.loc[1, "Memory"]],
                        hole=.3,
                        hoverinfo = 'label',
                        textinfo='value', 
                        textfont_size=20,
                    ),
                    row=2, col=3
                )
                fig.add_trace(
                    go.Pie(
                        labels = ['%d'%id1,'%d'%id2],
                        values = [df.loc[0, "Avg. Rating"], df.loc[1, "Avg. Rating"]],
                        hole=.3,
                        hoverinfo = 'label',
                        textinfo='value', 
                        textfont_size=20,
                    ),
                    row=2, col=4
                )
                  
                fig.update_layout(
                    height=800,
                    showlegend=True,
                    title_text="Compare laptops Id %d and Id %d"%(id1,id2),
                )
                fig.write_html('compare.html', auto_open = True)
            elif option == "3":
                statement = "SELECT Id,[Name],Brand,Size,Processor,Price,[Memory(GB)],Storage,Color,[Review Number],[Average Rating] FROM Laptops WHERE Id = %d"%id1
                result1 = list(cur.execute(statement).fetchone())
                statement = "SELECT Id,[Name],Brand,Size,Processor,Price,[Memory(GB)],Storage,Color,[Review Number],[Average Rating] FROM Laptops WHERE Id = %d"%id2
                result2 = list(cur.execute(statement).fetchone())
                with open('temp_compared.csv', 'w', newline='') as csvfile:
                    writer = csv.writer(csvfile, delimiter=',')
                    writer.writerow(result1) 
                    writer.writerow(result2) 
      
        else:
            print("Please correct your inputs!")

        print(load_help_text('mark_help2.txt'))
        command = input("Input your choice: ")
            
    conn.close()
    return marked_id


if __name__ == "__main__":
    # Figure out the very beginning interface:
    f = Figlet(font='slant')
    print(f.renderText(" Laptop World "))
    print ("%s%s Welcome to Yirui's database for laptops!!! %s\n" % (fg('white'), bg('cornflower_blue'), attr('reset')))
    print(load_help_text('help.txt'))
    option = input("Please select either 1 or 2 or 3 to choose your option: ")
    print("\n\n")

    # Print out help text if the user selects to stay in console:
    print(load_help_text('console_help.txt'))
    attri = input("Please choose the attribute(s) you want to focus on, or you can input 'exit' to quit: ")
    marked_id = []
    while attri != "exit":
        
        # Add marking functionality:
        marked_id = process_command(attri, marked_id, option)

        # Now is the marked interface:
        marked_id = marked_command(marked_id, option)

        print(load_help_text('console_help.txt'))
        attri = input("Please choose the attribute(s) you want to focus on, or you can input 'exit' to quit: ")
        if attri == "exit":
            print ("%s%s Hope you have a good time here! Bye! %s\n" % (fg('white'), bg('cornflower_blue'), attr('reset')))


