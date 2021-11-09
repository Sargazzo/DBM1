#!/usr/bin/python3

print('Content-type:text/html\n\n')
print('<html>')
print('<head>')
print('<title>Program Menu</title>')

#put the text in the middle
print('<style>')
print('h1 {text-align: center;}')
print('h2 {text-align: center;}')
print('div {text-align: center;}')
print('</style>')

print('</head>')

print('<body>')

print('<h1>The Paralympics Database</h1>')
print('<h2><a href="query1.cgi">For each of the sports how many athletes were enrolled in that discipline?</a></h2>')
print('<h2><a href="query2.cgi"><span style="text-align:center">Which first name was the 2nd most popular among the athletes?</a></h2>')
print('<h2><a href="query3.cgi"><span style="text-align:center">For each country, how many gold, silver and bronze medals did they win?</a></h2>')
print('<h2><a href="query4.cgi"><span style="text-align:center">For each year between 1980 and 1990, how many athletes were born in that year and what are their names?</a></h2>')
print('<h2><a href="query5.cgi"><span style="text-align:center">The birth year of athletes that won exactly 1 gold, 1 silver and 1 bronze medal?</a></h2>')
print('<h2><a href="query6.cgi"><span style="text-align:center">From all the winning teams across all events, which team has the most members and what are their names?</a></h2>')
print('<h2><a href="query7.cgi"><span style="text-align:center">Is there any female athlete that won any medal in two different disciplines across in two different editions?</a></h2>')
print('<h2><a href="query8.cgi"><span style="text-align:center">Is there any athlete that skipped one edition of the olympics but then performed better then his/her former participation in the same discipline?</a></h2>')

print('</body>')
print('</html>')


