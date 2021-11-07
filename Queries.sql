-- First Query -- Check
SELECT sport_code, COUNT(id) as participants FROM enrolled
GROUP BY sport_code;

-- Second Query -- It's incomplete if there are more people in first ath the same time or in second
SELECT first_name, COUNT(first_name) AS name_count
FROM person NATURAL JOIN athlete
WHERE first_name IS NOT NULL
GROUP BY(first_name)
ORDER BY name_count DESC
LIMIT 1 OFFSET 1;


-- This works - Cant eliminate the NULL value
SELECT first_name, COUNT(first_name)
    FROM person NATURAL JOIN athlete
    WHERE first_name IS NOT NULL AND first_name NOT IN
        (SELECT first_name
            FROM person NATURAL JOIN athlete
            WHERE first_name IS NOT NULL
            GROUP BY(first_name)
            HAVING COUNT(first_name) >=ALL(
                SELECT COUNT(first_name)
                FROM person NATURAL JOIN athlete
                WHERE first_name IS NOT NULL
                GROUP BY(first_name))
            )
    GROUP BY(first_name)
    HAVING COUNT(first_name) >= ALL(SELECT COUNT(first_name)
    FROM person NATURAL JOIN athlete
    WHERE first_name IS NOT NULL AND first_name NOT IN
        (SELECT first_name
            FROM person NATURAL JOIN athlete
            WHERE first_name IS NOT NULL
            GROUP BY(first_name)
            HAVING COUNT(first_name) >=ALL(
                SELECT COUNT(first_name)
                FROM person NATURAL JOIN athlete
                WHERE first_name IS NOT NULL
                GROUP BY(first_name))
            )
    GROUP BY(first_name)
    ORDER BY first_name DESC
    );

-- Third query -- still wrong, get each medal
SELECT c.name,COUNT(c.country_code) AS medal_num
FROM (medalists as m INNER JOIN  person as p
    ON m.id = p.id) as mp
    INNER JOIN COUNTRY as c ON c.country_code = mp.represents
WHERE mp.year = 2020
GROUP BY c.country_code
ORDER BY medal_num DESC;

-- Fourth Query -- Incomplete I dont know how to add the count and the names in the same table

SELECT last_name,first_name, a.date_of_birthday
FROM person as p NATURAL JOIN athlete as a
WHERE EXTRACT (YEAR FROM a.date_of_birthday) BETWEEN 1980 AND 1990
ORDER BY last_name;

SELECT COUNT(p.id) as num_of_athletes
FROM person as p NATURAL JOIN athlete as a
WHERE EXTRACT (YEAR FROM a.date_of_birthday) BETWEEN 1980 AND 1990;

-- Fifth Query -- Check
SELECT date_of_birthday
FROM athlete NATURAL JOIN person
WHERE id IN
        (SELECT id
        FROM medalists
        WHERE medal_type = 'Gold'
        GROUP BY id
        HAVING COUNT(id) = 1)
    AND id IN (SELECT id
        FROM medalists
        WHERE medal_type = 'Silver'
        GROUP BY id
        HAVING COUNT(id) = 1)
    AND id IN (SELECT id
        FROM medalists
        WHERE medal_type = 'Bronze'
        GROUP BY id
        HAVING COUNT(id) = 1);


-- Sixth Query -- CHECK

-- Get the team events with the most number of players and their names
SELECT pa.first_name, pa.last_name, m.event_name, m.sport_code
FROM (person NATURAL JOIN athlete) AS pa
    INNER JOIN medalists AS m ON pa.id = m.id
WHERE m.medal_type = 'Gold' AND (m.event_name,m.sport_code) IN
    (SELECT event_name, sport_code
    FROM medalists
    WHERE medal_type = 'Gold'
    GROUP BY (event_name, sport_code)
    HAVING COUNT(*) >= ALL(
        SELECT COUNT(*)
        FROM medalists
        WHERE medal_type = 'Gold'
        GROUP BY (event_name, sport_code)
    )
);


-- The team sports with most players
SELECT event_name, sport_code, COUNT(*) as count
FROM medalists
WHERE medal_type = 'Gold'
GROUP BY (event_name, sport_code)
HAVING COUNT(*) >= ALL(
    SELECT COUNT(*)
    FROM medalists
    WHERE medal_type = 'Gold'
    GROUP BY (event_name, sport_code)
);

-- All team sports
SELECT event_name, sport_code, COUNT(*) as count
FROM medalists
WHERE medal_type = 'Gold'
GROUP BY (event_name, sport_code)
HAVING COUNT(*) > 1
ORDER BY count DESC;

-- Seventh Query --

-- NEEDS SPECIFIC INPUTS

SELECT first_name,last_name
FROM person NATURAL JOIN athlete NATURAL JOIN medalists
WHERE gender = 'F' AND id IN

-- Eighth Query --

-- NEEDS SPECIFIC INPUTS






