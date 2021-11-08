----------------------
--Tables' Clear:
----------------------
DROP TABLE if EXISTS medalists CASCADE;
DROP TABLE if EXISTS event CASCADE;
DROP TABLE if EXISTS enrolled CASCADE;
DROP TABLE if EXISTS sport CASCADE;
DROP TABLE if EXISTS represents CASCADE;
DROP TABLE if EXISTS athlete CASCADE;
DROP TABLE if EXISTS coach CASCADE;
DROP TABLE if EXISTS person CASCADE;
DROP TABLE if EXISTS country CASCADE;

-------------------
--TABLES CREATION--
-------------------


CREATE TABLE country(
    country_code VARCHAR (3),
    name VARCHAR(75),
    total_medal_rank INT,
    gold_medal_count INT,
    silver_medal_count INT,
    bronze_medal_count INT,
    PRIMARY KEY (country_code)
);

CREATE TABLE person(
    id INT GENERATED BY DEFAULT AS IDENTITY
        (START WITH 1 INCREMENT BY 1) NOT NULL UNIQUE,
    first_name VARCHAR(50),
    last_name VARCHAR(75),
    represents VARCHAR(3),
    PRIMARY KEY (id),
    FOREIGN KEY (represents) REFERENCES country(country_code)
);

CREATE TABLE coach(
    id INT NOT NULL,
    PRIMARY KEY (id),
    FOREIGN KEY (id) REFERENCES person (id)
);

CREATE TABLE athlete(
    id INT NOT NULL,
    date_of_birthday DATE,
    gender CHAR,
    PRIMARY KEY (id),
    FOREIGN KEY (id) REFERENCES person (id)
);
-- Constraint gender follows a format
ALTER TABLE athlete ADD CONSTRAINT valid_gender CHECK(
        gender= 'F' OR
        gender = 'M');


-------------------------------------
-- Sports/Disciplines Table --

CREATE TABLE sport(
    sport_code VARCHAR(3),
    name VARCHAR(50),
    male_num INT,
    female_num INT,
    PRIMARY KEY (sport_code)
);
-- The primary key is a combination of the year, the sport and the person
CREATE TABLE enrolled(
    sport_code VARCHAR(3),
    id INT,
    year INT,
    PRIMARY KEY (sport_code, id, year),
    FOREIGN KEY (id) REFERENCES person (id),
    FOREIGN KEY (sport_code) REFERENCES sport (sport_code)
);

-- Weak entity event from sport
CREATE TABLE event(
    sport_code VARCHAR(3),
    name VARCHAR(50),
    PRIMARY KEY (sport_code,name),
    FOREIGN KEY (sport_code) REFERENCES sport (sport_code)
);

-- mealists table
CREATE TABLE medalists(
    sport_code VARCHAR(3),
    event_name VARCHAR(50),
    id INT,
    medal_type VARCHAR(6),
    year INT,
    PRIMARY KEY (sport_code,event_name,id,year),
    FOREIGN KEY (sport_code, event_name) REFERENCES event (sport_code,name),
    FOREIGN KEY (id,year,sport_code) REFERENCES enrolled (id,year,sport_code)
);

-- Verify if the medal inserted is valid
ALTER TABLE medalists ADD CONSTRAINT valid_medal CHECK(
        medal_type = 'Gold' OR
        medal_type = 'Silver' OR
        medal_type = 'Bronze');