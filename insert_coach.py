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
        
        # Remove the space before the beginning of the word
        first_name = work_line[1]
        last_name = work_line[2]
        country_code = work_line[4]
        sport_code = work_line[6]
                
        # Verify if the coach exists already in the table
        sql_verify_person = 'SELECT id from person NATURAL JOIN coach WHERE first_name = %s AND last_name = %s AND represents = %s;'
        
        verify_data = (first_name, last_name, country_code)
        
        cursor.execute(sql_verify_person, verify_data)
        verify = cursor.fetchone()
        
        #If that coach already exists in the data we are introducing - just add to enrolled table
        if verify:
            
            
            #Get the ID
            for personID in verify:
                break
            
            sql_verify_coach = 'Select sport_code, year FROM enrolled WHERE id = %s;'
            cursor.execute(sql_verify_coach, [personID])
            
            info = cursor.fetchone()
            
            # If the coach is inserted already but with a different gender
            if sport_code == info[0] and 2020 == info[1]:
                continue
            
            else:
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
            
            data_person = (first_name,last_name, country_code)
        
            # Feed the data to the SQL query as follows to avoid SQL injection
            cursor.execute(sql_person, data_person)
            
            #Get the inserted ID
            sql_get_person_ID = 'SELECT MAX(id) from person;'
            
            #Executes the query
            cursor.execute(sql_get_person_ID)
            
            #Gets the ID from the new person inserted
            ID = cursor.fetchone()
            
            #Get the current ID
            for personID in ID:
                break    

            #Insert values in coach table
            sql_coach = 'INSERT INTO coach VALUES (%s);'
            
            cursor.execute(sql_coach, [personID])
            
            #Inserting in enrolled table
            sql_enrolled = 'INSERT INTO enrolled VALUES (%s, %s, 2020);'
    
            data_enrolled = (sport_code, personID)
            
            cursor.execute(sql_enrolled, data_enrolled)
    
        	
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
