#!/usr/bin/python3

import psycopg2
import login

print('Content-type:text/html\n\n')
print('<html>')
print('<head>')
print('<title>Query 7</title>')
print('</head>')
print('<body>')

connection = None
try:
    # Creating connection
    connection = psycopg2.connect(login.credentials)
    print('<h1>Female medalists across different years in different disciplines</h1>')
    cursor = connection.cursor()

    # Making query
    sql_query = ('SELECT DISTINCT(winner.id), winner.first_name,winner.last_name FROM (person NATURAL JOIN athlete NATURAL JOIN medalists) AS winner WHERE winner.gender = %s AND winner.id IN( SELECT id FROM medalists AS m WHERE m.id = winner.id AND m.year != winner.year AND m.sport_code != winner.sport_code ) ORDER BY winner.id;')
    cursor.execute(sql_query,['F'])
    result = cursor.fetchall()
    num = len(result)

    # Displaying results
    print('<table border="5">')
    print('<tr>')
    print('<td>id</td><td>First Name</td><td>Last Name</td>')
    print('</tr>')

    for row in result:
        print('<tr>')
        for value in row:
            # The string has the {}, the variables inside format() will replace the {}
            print('<td>{}</td>'.format(value))
        print('</tr>')
    print('</table>')

    ## Second table

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
