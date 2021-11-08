-- First Query -- Katharina corrected it
SELECT name, sport_code, COUNT(DISTINCT(id)) AS participants
FROM enrolled NATURAL JOIN sport
GROUP BY (name,sport_code)
ORDER BY participants DESC;

SELECT name,(male_num + female_num) AS num_of_athletes
FROM sport
ORDER BY num_of_athletes DESC;

-- Second Query --

-- This works when all the names are repeated different number times
SELECT first_name, COUNT(first_name) AS name_count
FROM person NATURAL JOIN athlete
WHERE first_name IS NOT NULL
GROUP BY(first_name)
ORDER BY name_count DESC
LIMIT 1 OFFSET 1;


-- This works for all cases
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

CREATE INDEX first_name_index ON person USING hash (first_name);
DROP INDEX first_name_index;

-- Third query -- Check - each

SELECT name, gold_medal_count, silver_medal_count, bronze_medal_count
FROM COUNTRY
ORDER BY total_medal_rank ASC;

-- Fourth Query -- Incomplete I dont know how to add the count and the names in the same table

SELECT last_name,first_name, a.date_of_birthday
FROM person as p NATURAL JOIN athlete as a
WHERE EXTRACT (YEAR FROM a.date_of_birthday) BETWEEN 1980 AND 1990
ORDER BY last_name;

SELECT COUNT(p.id) as num_of_athletes
FROM person as p NATURAL JOIN athlete as a
WHERE EXTRACT (YEAR FROM a.date_of_birthday) BETWEEN 1980 AND 1990;

-- Indexing B-Tree

CREATE INDEX birthday ON athlete USING btree (date_of_birthday);
DROP index birthday;

-- Fifth Query -- Check
SELECT EXTRACT (YEAR FROM date_of_birthday)
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

SELECT DISTINCT(winner.id), winner.first_name,winner.last_name
FROM (person NATURAL JOIN athlete NATURAL JOIN medalists) AS winner
WHERE winner.gender = 'F' AND winner.id IN(
    SELECT id
    FROM medalists AS m
    WHERE m.id = winner.id AND m.year != winner.year AND m.sport_code != winner.sport_code
    )
ORDER BY winner.id;

-- Eighth Query --

-- NEEDS SPECIFIC INPUTS

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


-- Index to accelarate querie
CREATE INDEX enrolled_index ON enrolled USING hash (year);
CREATE INDEX medalists_index ON medalists USING hash (year);
DROP index enrolled_index;
DROP index medalists_index;

INSERT INTO enrolled VALUES('JUD',1,2028);
INSERT INTO enrolled VALUES('JUD',1,2024);
DELETE FROM enrolled where id = 1 AND year = 2024;
INSERT INTO medalists VALUES('JUD','Men -100 kg',1,'Gold', 2028);
DELETE FROM medalists where id = 1 AND year = 2028;

INSERT INTO enrolled VALUES('ARC',1,2028);
INSERT INTO medalists VALUES('ARC','Men''s Individual - W1',1,'Gold', 2028);

SELECT * FROM medalists where id = 1;
SELECT * FROM enrolled where id = 1;

-- Test 7th query
INSERT INTO enrolled VALUES('WBK',8,2012);
INSERT INTO medalists VALUES('WBK','Women',8,'Gold', 2012);

INSERT INTO enrolled VALUES('WBK',8,2014);
INSERT INTO medalists VALUES('WBK','Women',8,'Gold', 2014);

INSERT INTO enrolled VALUES('ARC',8,2014);
INSERT INTO medalists VALUES('ARC','Women''s Individual - W1',8,'Gold', 2014);



