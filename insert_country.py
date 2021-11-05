# -*- coding: utf-8 -*-
"""
Created on Fri Nov  5 15:02:15 2021

@author: Utilizador
"""

import psycopg2
import cgi
import pathlib

connection = None


#Directory of the file with the data
medalist_countries_dir = str(pathlib.Path(__file__).parent.absolute()) + '/Real Data/paralympic-medal-tally.csv'
all_countries_dir = str(pathlib.Path(__file__).parent.absolute()) + '/Real Data/NPCs-list.csv'

#Opens the file with info
medalist_countries = open(medalist_countries_dir, "r")
all_countries = open(all_countries_dir, "r")

#The first line contains no information
first = 0;


try:
	# Creating connection
    connection = psycopg2.connect(host = 'localhost',
                                user = 'postgres',
                                port = 5432,
                                dbname = 'postgres')
    
    #Creates the Cursor
    cursor = connection.cursor()
    
    #Reading each line of the file with the athlete data
    for line in all_countries:
        
        #The first line is ignored
        if first == 0:
            first = -1
            continue
        
        #Removes the paragraph symbol and separates the info by each comma
        work_line = line.split("\n")[0]
        work_line = work_line.split(",")
                
        #Inserting in person table
        sql_country = 'INSERT INTO country VALUES (%s,%s,%s,%s,%s,%s);'
        
        #Initialize the countries as last ranking with 0 medals
        if work_line[0][1:] == 'Hong Kong' or work_line[0][1:] == 'Virgin Islands':
            identification = (work_line[2], work_line[0][1:] + "," + work_line[1][:-1],"87","0","0","0")
            
        else:
            #Getting the country code and its name
            identification = (work_line[1],work_line[0],"87","0","0","0")
            
        # Feed the data to the SQL query as follows to avoid SQL injection
        cursor.execute(sql_country, identification)
        
        # Commit the update (without this step the database will not change)
        connection.commit()
        
    ################ Updating the countries to its true medal ranking ###################
    
    #Reset the flag
    first = 0;
    #Reading each line of the file with the athlete data
    for line in medalist_countries:
        
        #The first line is ignored
        if first == 0:
            first = -1
            continue
        
        #Removes the paragraph symbol and separates the info by each comma
        work_line = line.split("\n")[0]
        work_line = work_line.split(",")
        
        
        #Get the rank
        rank = work_line[0]
        
        #Get the medal number for each country
        
        #If it is a country with a compose name
        if work_line[1][1:] == 'Hong Kong' or work_line[1][1:] == 'Virgin Islands':
             code = work_line[3]
             gold = work_line[4]
             silver = work_line[5]
             bronze = work_line[6]
            
        else:
            code = work_line[2]
            gold = work_line[3]
            silver = work_line[4]
            bronze = work_line[5]
            
        
    
        sql_country_update = 'UPDATE country SET total_medal_rank = %s, gold_medal_count = %s, silver_medal_count = %s, bronze_medal_count = %s WHERE country_code = %s;'
    
        update_data = (rank, gold, silver, bronze,code)
        
        # Feed the data to the SQL query as follows to avoid SQL injection
        cursor.execute(sql_country_update, update_data)
        
        # Commit the update (without this step the database will not change)
        connection.commit()

#If something goes wrong
except Exception as error_description:
	print(error_description)
	cursor.close()

finally:
	if connection is not None:
		connection.close()

# Closes the file
medalist_countries.close()
all_countries.close()