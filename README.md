# DBM1
This is the repository used to organized and build our DBM1: Databases and Data Mining project as part of Riccardo Tommassini's class at INSA Lyon. 

We retrieved the underlying dataset of our project from kaggle:
https://www.kaggle.com/shivagovindasamy/2020-tokyo-paralympics

It contains information on the 2020 Tokyo Paralympics. More specifically, an abundant amount of data on athletes, coaches, sports, events, etc is present.

We have made certain design choices and visualized them in an ER diagram, as it can be seen in the er-diagram.png file.

We performed preprocessing on the data to format it according to our needs using the preprocessing.py file.

To create the relevant tables in the database, execute the paralympics.sql file.

When populating the database using the 'insert'-files, make sure to execute them in the following order: country, sports,person, athlete, coach,enrolled, events and medalists.

Done!

To see the implementation of our SQL queries, have a look at 'Queries.sql'.

We have also a website to visualize the queries:

https://web.tecnico.ulisboa.pt/ist190114/main.cgi
