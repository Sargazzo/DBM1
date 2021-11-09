#!/usr/bin/python3

import psycopg2
import login

print('Content-type:text/html\n\n')
print('<html>')
print('<head>')
print('<title>Query 4</title>')
print('</head>')
print('<body>')

connection = None
try:
    # Creating connection
    connection = psycopg2.connect(login.credentials)
    print('<h1>Athletes that were born between 1980 and 1990</h1>')
    cursor = connection.cursor()

    # Making query
    sql_query = ('SELECT COUNT(p.id) as num_of_athletes FROM person as p NATURAL JOIN athlete as a WHERE EXTRACT (YEAR FROM a.date_of_birthday) BETWEEN 1980 AND 1990;')
    cursor.execute(sql_query)
    result = cursor.fetchall()
    num = len(result)

    # Displaying results
    print('<table border="5">')
    print('<tr>')
    print('<td>Number of athletes</td>')
    print('</tr>')

    for row in result:
        print('<tr>')
        for value in row:
            # The string has the {}, the variables inside format() will replace the {}
            print('<td>{}</td>'.format(value))
        print('</tr>')
    print('</table>')

    ## Second table

    # Making query
    sql_query = ('SELECT first_name, last_name, a.date_of_birthday FROM person as p NATURAL JOIN athlete as a WHERE EXTRACT (YEAR FROM a.date_of_birthday) BETWEEN 1980 AND 1990 ORDER BY date_of_birthday;')
    cursor.execute(sql_query)
    result = cursor.fetchall()
    num = len(result)

    # Displaying results
    print('<table border="5">')
    print('<tr>')
    print('<td>First name</td><td>Last name</td><td>Date of birthday</td>')
    print('</tr>')

    for row in result:
        print('<tr>')
        for value in row:
            # The string has the {}, the variables inside format() will replace the {}
            print('<td>{}</td>'.format(value))
        print('</tr>')
    print('</table>')

    # Closing connection
    cursor.close()

except Exception as error_description:
    print('<h1>An error occurred.</h1>')
    print('<p>{}</p>'.format(error_description))
finally:
    if connection is not None:
        connection.close()

print('<p><a href="https://web.tecnico.ulisboa.pt/ist190114/main.cgi">Return</a></p>')

print('</body>')
print('</html>')
