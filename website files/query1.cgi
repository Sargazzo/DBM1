#!/usr/bin/python3

import psycopg2
import login

print('Content-type:text/html\n\n')
print('<html>')
print('<head>')
print('<title>Query 1</title>')
print('</head>')
print('<body>')

connection = None
try:
    # Creating connection
    connection = psycopg2.connect(login.credentials)
    print('<h1>List of athletes enrolled per discipline</h1>')
    cursor = connection.cursor()

    # Making query
    sql_query = 'SELECT name,sport_code, COUNT(DISTINCT(id)) AS participants FROM enrolled NATURAL JOIN sport GROUP BY (name,sport_code) ORDER BY participants DESC;'
    cursor.execute(sql_query)
    result = cursor.fetchall()
    num = len(result)

    # Displaying results
    print('<table border="5">')
    print('<tr>')
    print('<td>Sport Name</td><td>Sport Code</td><td>Participants</td>')
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
