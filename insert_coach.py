# -*- coding: utf-8 -*-
"""
Created on Wed Nov  3 18:50:06 2021

@author: Utilizador
"""

import psycopg2
import cgi
import pathlib

connection = None


file_dir = str(pathlib.Path(__file__).parent.absolute()) + '/Real Data/coaches-preprocessed.csv'

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
                
       #Inserting in person table
        sql_person = 'INSERT INTO person VALUES (DEFAULT, %s, %s, %s);'
        
        data_person = (work_line[1],work_line[2], work_line[4])
       
        # Feed the data to the SQL query as follows to avoid SQL injection
        cursor.execute(sql_person, data_person)
        
        #GET The ID of the new person
        sql_get_person_ID = 'SELECT MAX(id) from person;'
        
        #Executes the query
        cursor.execute(sql_get_person_ID)
        
        #Gets the ID from the new person inserted
        ID = cursor.fetchone()
        
        #Get the current ID
        for personID in ID:
            break
        
        sql_verify_person = 'SELECT id from person NATURAL JOIN coach WHERE first_name = %s AND last_name = %s;'
        
        verify_data = (first_name, last_name, country_code)
        
        cursor.execute(sql_verify_person, verify_data)
        verify = cursor.fetchone()
        
        #If that player already exists in the data we are introducing - just add to enrolled table
        if verify:
            
            #Get the ID
            for personID in verify:
                break
            #Inserting in enrolled table
            sql_enrolled = 'INSERT INTO enrolled VALUES (%s, %s, 2020);'
    
            data_enrolled = (sport_code, personID)
            
            cursor.execute(sql_enrolled, data_enrolled)
    
        	
        	# Commit the update (without this step the database will not change)
            connection.commit()
            
        #New insert
        else:
            #Inserting in person table
            sql_person = 'INSERT INTO person VALUES (DEFAULT, %s, %s, %s);'
            
            data_person = (work_line[1],work_line[2], work_line[4])
        
            # Feed the data to the SQL query as follows to avoid SQL injection
            cursor.execute(sql_person, data_person)
            
            #Gets the ID from the new person inserted
            ID = cursor.fetchone()
            
            #Get the current ID
            for personID in ID:
                break
    

        #Insert values in coach table
        sql_coach = 'INSERT INTO coach VALUES (%s);'

        data_coach = (personID,)
    
        cursor.execute(sql_coach, data_coach)
        
    	
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