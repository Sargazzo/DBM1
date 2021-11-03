# -*- coding: utf-8 -*-
"""
Created on Wed Nov  3 18:50:06 2021

@author: Utilizador
"""

import psycopg2
import cgi

connection = None

try:
	# Creating connection
	connection = psycopg2.connect(host = 'localhost',
                                    user = 'postgres',
                                    port = 5432,
                                    dbname = 'postgres')
	cursor = connection.cursor()

	# Making query
	sql_person = 'INSERT INTO person VALUES (DEFAULT, %s, %s);'
	data = ('Joao','Marques')

	# Feed the data to the SQL query as follows to avoid SQL injection
	cursor.execute(sql_person, data)
	
	# Commit the update (without this step the database will not change)
	connection.commit()

#If something goes wrong
except Exception as error_description:
	print(error_description)
	cursor.close()

finally:
	if connection is not None:
		connection.close()