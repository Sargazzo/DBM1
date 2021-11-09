#!/usr/bin/python3

import psycopg2
import login

print('Content-type:text/html\n\n')
print('<html>')
print('<head>')
print('<title>Query 6</title>')
print('</head>')
print('<body>')

connection = None
try:
    # Creating connection
    connection = psycopg2.connect(login.credentials)
    print('<h1>Teams with the most player number among all the winning teams</h1>')
    cursor = connection.cursor()

    # Making query
    sql_query = ('SELECT pa.first_name, pa.last_name, m.event_name, m.sport_code FROM (person NATURAL JOIN athlete) AS pa INNER JOIN medalists AS m ON pa.id = m.id WHERE m.medal_type = %s AND (m.event_name,m.sport_code) IN (SELECT event_name, sport_code FROM medalists WHERE medal_type = %s GROUP BY (event_name, sport_code) HAVING COUNT(*) >= ALL( SELECT COUNT(*) FROM medalists WHERE medal_type = %s GROUP BY (event_name, sport_code) ) );')
    cursor.execute(sql_query,['Gold','Gold','Gold'])
    result = cursor.fetchall()
    num = len(result)

    # Displaying results
    print('<table border="5">')
    print('<tr>')
    print('<td>First Name</td><td>Last Name</td><td>Event Name</td><td>Sport Code</td>')
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
