# -*- coding: utf-8 -*-
"""
Created on Sat Nov  6 03:13:24 2021

@author: Utilizador
"""

import psycopg2
import cgi
import pathlib
import login
from tqdm import tqdm
connection = None


#Directory of the file with the data
file_dir = str(pathlib.Path(__file__).parent.absolute()) + '/Real Data/paralympic-medals.csv'

#Opens the file with info
file = open(file_dir, "r")

#The first line contains no information
first = 0;


try:
	# Creating connection
    connection = psycopg2.connect(login.credentials)
    cursor = connection.cursor()
    
    #Reading each line of the file with the athlete data
    for line in tqdm(file):
        
        #The first line 
        if first == 0:
            first = -1
            continue
        
        # Separate the information of the line
        work_line = line.split("\n")[0]
        work_line = work_line.split(",")
        
        #Get the other needed data
        if work_line[0][1:] == 'Hong Kong' or work_line[0][1:] == 'Virgin Islands':
            country_code = work_line[2]
            full_name = work_line[3]
            sport_code = work_line[5]
            event_name = work_line[6]
            medal = work_line[7].split(" ")[0]
            
        #Countries without a comma in its name
        else:
            country_code = work_line[1]
            full_name = work_line[2]
            sport_code = work_line[4]
            event_name = work_line[5]
            medal = work_line[6].split(" ")[0]
        
        # Separate the player name into last name and first name
        
        words = full_name.split()
        lastname = ''
        firstname = ''
        for word in words:  
            if word.isupper():
                if lastname == '':
                    lastname = word
                else:
                    lastname = lastname + " " + word
            else:
                if firstname == '':
                    firstname = word
                else:
                    firstname = firstname + " " + word
            
        # Get the person ID
        
        sql_get_id = 'SELECT id from person NATURAL JOIN enrolled WHERE first_name = %s AND last_name = %s AND sport_code = %s AND represents = %s;'
        
        
        get_id = (firstname, lastname,sport_code, country_code)
        
        cursor.execute(sql_get_id, get_id)
        
        #Gets the ID from the new person inserted
        ID = cursor.fetchone()
        
        #Get the current ID
        for personID in ID:
            break
                
        sql_verify_event = 'SELECT name from event WHERE name = %s AND sport_code = %s;'
        
        verify_data = (event_name, sport_code)
        
        cursor.execute(sql_verify_event, verify_data)
        verify = cursor.fetchone()
           
        #If the event already exists, just add to the medalist table
        if not verify:
            sql_insert_event = 'INSERT INTO event VALUES (%s,%s)'
            
            event_data = (sport_code, event_name)
            
            cursor.execute(sql_insert_event, event_data)
            
            connection.commit()
            
            
        #Inserting in enrolled table
        sql_medalist= 'INSERT INTO medalists VALUES (%s,%s,%s,%s,2020);'
   
        data_medalist = (sport_code, event_name,personID,medal)
       
        cursor.execute(sql_medalist, data_medalist)
   
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
file.close()