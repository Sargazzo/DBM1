#!/usr/bin/python3

import psycopg2
import login

print('Content-type:text/html\n\n')
print('<html>')
print('<head>')
print('<title>Query 5</title>')
print('</head>')
print('<body>')

connection = None
try:
    # Creating connection
    connection = psycopg2.connect(login.credentials)
    print('<h1>Athletes that won 1 gold medal, 1 silver medal and 1 bronze medal</h1>')
    cursor = connection.cursor()

    # Making query
    sql_query = ('SELECT Distinct(EXTRACT (YEAR FROM date_of_birthday)) FROM athlete NATURAL JOIN person WHERE id IN (SELECT id FROM medalists WHERE medal_type = %s GROUP BY id HAVING COUNT(id) = 1) AND id IN (SELECT id FROM medalists WHERE medal_type = %s GROUP BY id HAVING COUNT(id) = 1) AND id IN (SELECT id FROM medalists WHERE medal_type = %s GROUP BY id HAVING COUNT(id) = 1);')
    cursor.execute(sql_query,['Gold','Silver','Bronze'])
    result = cursor.fetchall()
    num = len(result)

    # Displaying results
    print('<table border="5">')
    print('<tr>')
    print('<td>Birthday Year</td>')
    print('</tr>')

    for row in result:
        print('<tr>')
        for value in row:
            value = int(value)
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
