#!/usr/bin/python3

import psycopg2
import login

print('Content-type:text/html\n\n')
print('<html>')
print('<head>')
print('<title>Query 8</title>')
print('</head>')
print('<body>')

connection = None
try:
    # Creating connection
    connection = psycopg2.connect(login.credentials)
    print('<h1>Athlete that did not win a medal at one session, skipped the following and that in the next one won a medal</h1>')
    cursor = connection.cursor()

    # Making query
    sql_query = ('SELECT DISTINCT(init.id), init.first_name,init.last_name,init.sport_code FROM (person NATURAL JOIN athlete NATURAL JOIN enrolled) AS init WHERE init.id IN( SELECT e.id FROM (SELECT id FROM enrolled WHERE year = init.year AND sport_code = init.sport_code) AS e INNER JOIN (SELECT id from medalists WHERE year = init.year + 8 AND sport_code = init.sport_code) AS win ON e.id = win.id EXCEPT(SELECT m.id FROM medalists AS m WHERE m.year = init.year AND m.sport_code = init.sport_code) ) AND init.id NOT IN( SELECT id FROM enrolled WHERE year = (init.year + 4) ) ORDER BY init.id ASC;')
    cursor.execute(sql_query,['F'])
    result = cursor.fetchall()
    num = len(result)

    # Displaying results
    print('<table border="5">')
    print('<tr>')
    print('<td>id</td><td>First Name</td><td>Last Name</td><td>Sport Code</td>')
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
