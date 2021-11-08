-- First Query -- Katharina corrected it
SELECT name, sport_code, COUNT(DISTINCT(id)) AS participants
FROM enrolled NATURAL JOIN sport
GROUP BY (name,sport_code)
ORDER BY participants DESC;

-- Second Query --

-- This works when all the names are repeated different number times
-- eg if there is just 1 most common name and one second most common name
SELECT first_name, COUNT(first_name) AS name_count
FROM person NATURAL JOIN athlete
WHERE first_name IS NOT NULL
GROUP BY(first_name)
ORDER BY name_count DESC
LIMIT 1 OFFSET 1;


-- This is the query that works for all the cases
SELECT first_name, COUNT(first_name)
    FROM person NATURAL JOIN athlete
    WHERE first_name != '' AND first_name NOT IN
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

-- Index : name, table, type of index, collumn
CREATE INDEX first_name_index ON person USING hash (first_name);
DROP INDEX first_name_index;

-- Third query --

SELECT name, gold_medal_count, silver_medal_count, bronze_medal_count
FROM COUNTRY
ORDER BY total_medal_rank ASC;

-- Fourth Query -- Those are basically 2 queries

-- Names of the athletes
SELECT last_name,first_name, a.date_of_birthday
FROM person as p NATURAL JOIN athlete as a
WHERE EXTRACT (YEAR FROM a.date_of_birthday) BETWEEN 1980 AND 1990
ORDER BY a.date_of_birthday;

-- Total number
SELECT COUNT(p.id) as num_of_athletes
FROM person as p NATURAL JOIN athlete as a
WHERE EXTRACT (YEAR FROM a.date_of_birthday) BETWEEN 1980 AND 1990;

-- Indexing B-Tree
CREATE INDEX birthday ON athlete USING btree (date_of_birthday);
DROP index birthday;

-- Fifth Query -- Check
SELECT DISTINCT(EXTRACT (YEAR FROM date_of_birthday)) AS year_of_birthday
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


-- Sixth Query --

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

-- Seventh Query --

SELECT DISTINCT(winner.id), winner.first_name,winner.last_name
FROM (person NATURAL JOIN athlete NATURAL JOIN medalists) AS winner
WHERE winner.gender = 'F' AND winner.id IN(
    SELECT id
    FROM medalists AS m
    WHERE m.id = winner.id AND m.year != winner.year AND m.sport_code != winner.sport_code
    )
ORDER BY winner.id;

-- Eighth Query --

-- Assumptions: taken into account that performance improvement is not receiving a medal to receiving a medal
SELECT DISTINCT(init.id), init.first_name,init.last_name,init.sport_code
FROM (person NATURAL JOIN athlete NATURAL JOIN enrolled) AS init
WHERE init.id IN(
        SELECT e.id
        FROM (SELECT id FROM enrolled WHERE year = init.year AND sport_code = init.sport_code) AS e -- Enrolled in the first year
            INNER JOIN (SELECT id from medalists WHERE year = init.year + 8 AND sport_code = init.sport_code) AS win -- Winner 3rd edition
            ON e.id = win.id
            EXCEPT(SELECT m.id -- Not medalist in the first year
               FROM medalists AS m
               WHERE m.year = init.year AND m.sport_code = init.sport_code)
        )
    AND init.id NOT IN( -- not enrolled in the 2nd edition
        SELECT id
        FROM enrolled
        WHERE year = (init.year + 4)
    )
ORDER BY init.id ASC;

-- Index : name, table, type of index, collumn
CREATE INDEX enrolled_index ON enrolled USING hash (year);
CREATE INDEX medalists_index ON medalists USING hash (year);
DROP index enrolled_index;
DROP index medalists_index;




