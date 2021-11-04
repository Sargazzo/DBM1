# -*- coding: utf-8 -*-
"""
Created on Wed Nov  3 18:50:06 2021

@author: Utilizador
"""

import psycopg2
import cgi
import pathlib

connection = None



file_dir = str(pathlib.Path(__file__).parent.absolute()) + '/athletes-preprocessed.csv'

file = open(file_dir, "r")

first = 0;


try:
	# Creating connection
    connection = psycopg2.connect(host = 'localhost',
                                user = 'postgres',
                                port = 5432,
                                dbname = 'postgres')
    cursor = connection.cursor()
    
    for line in file:
        
        #The first line 
        if first == 0:
            first = -1
            continue
        work_line = line.split("\n")[0]
        work_line = work_line.split(",")
                
        #Making query
        sql_person = 'INSERT INTO person VALUES (DEFAULT, %s, %s);'
        data = (work_line[1],work_line[2])
        
        # Feed the data to the SQL query as follows to avoid SQL injection
        cursor.execute(sql_person, data)
        
        #GET The ID of the new person
        sql_get_person_ID = 'SELECT MAX(id) from person;'
        
        cursor.execute(sql_get_person_ID)
        	
        ID = cursor.fetchone()
        
        #Get the current ID
        for personID in ID:
            break
       
        #Insert values in athlete table
        sql_athlete = 'INSERT INTO athlete VALUES (%s, %s, %s);'
        
        #The Hong Kong and Virgin Islands Countries have a comma in the name

        if work_line[3][1:] == 'Hong Kong' or work_line[3][1:] == 'Virgin Islands':
            data_new = (personID, work_line[8], work_line[9])
            
        else:
            data_new = (personID, work_line[7], work_line[8])
        cursor.execute(sql_athlete, data_new)
        
    	
    	# Commit the update (without this step the database will not change)
        connection.commit()
    
    

#If something goes wrong
except Exception as error_description:
	print(error_description)
	cursor.close()

finally:
	if connection is not None:
		connection.close()

file.close()