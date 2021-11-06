# -*- coding: utf-8 -*-
"""
Created on Wed Nov  3 18:50:06 2021

@author: Utilizador
"""

import psycopg2
import cgi
import pathlib

connection = None


#Directory of the file with the data
file_dir = str(pathlib.Path(__file__).parent.absolute()) + '/Real Data/athletes-preprocessed.csv'

#Opens the file with info
file = open(file_dir, "r")

#The first line contains no information
first = 0;


try:
	# Creating connection
    connection = psycopg2.connect(host = 'localhost',
                                user = 'postgres',
                                port = 5432,
                                dbname = 'postgres')
    cursor = connection.cursor()
    
    #Reading each line of the file with the athlete data
    for line in file:
        
        #The first line 
        if first == 0:
            first = -1
            continue
        work_line = line.split("\n")[0]
        work_line = work_line.split(",")
        
        #Get the athlete name
        first_name = work_line[1]
        last_name = work_line[2]
        
        #Get the other needed data
        if work_line[3][1:] == 'Hong Kong' or work_line[3][1:] == 'Virgin Islands':
            country_code = work_line[5]
            sport_code = work_line[7]
            birthday = work_line[8]
            gender = work_line[9][0]
            
        #Countries without a comma in its name
        else:
            country_code = work_line[4]
            sport_code = work_line[6]
            country_code = work_line[4]
            birthday = work_line[7]
            gender = work_line[8][0]
                
        sql_verify_person = 'SELECT id from person NATURAL JOIN athlete WHERE first_name = %s AND last_name = %s AND date_of_birthday = %s AND represents = %s;'
        
        verify_data = (first_name, last_name, birthday, country_code)
        
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
            
            data_person = (first_name, last_name, country_code)
            
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
    
    
            #Insert values in athlete table
            sql_athlete = 'INSERT INTO athlete VALUES (%s, %s, %s);'
            
            data_athlete = (personID,birthday,gender)
    
            cursor.execute(sql_athlete, data_athlete)
        
    
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

# Closes the file
file.close()
