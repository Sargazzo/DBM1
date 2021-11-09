# -*- coding: utf-8 -*-
"""
Created on Wed Nov  3 18:50:06 2021

@author: Utilizador
"""

import psycopg2
import cgi
import pathlib
import login
connection = None


file_dir = str(pathlib.Path(__file__).parent.absolute()) + '/Real Data/entries-by-discipline.csv'

file = open(file_dir, "r")

first = 0;


try:
	# Creating connection
    connection = psycopg2.connect(login.credentials)
    cursor = connection.cursor()
    
    for line in file:
        
        #The first line 
        if first == 0:
            first = -1
            continue
        work_line = line.split("\n")[0]
        work_line = work_line.split(",")
                
        #Making query
        sql_sport = 'INSERT INTO sport VALUES (%s, %s, %s, %s);'
        data = (work_line[1],work_line[0], work_line[3], work_line[2])
        
        # Feed the data to the SQL query as follows to avoid SQL injection
        cursor.execute(sql_sport, data)
        
    	
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