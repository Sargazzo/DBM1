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
    id SERIAL,
    last_name VARCHAR(75),
    PRIMARY KEY (id)
);

CREATE TABLE coach(
    id INT,
    PRIMARY KEY (id),
    FOREIGN KEY (id) REFERENCES person (id)
);

CREATE TABLE athlete(
    id INT,
    date_of_birthday DATE,
    gender CHAR,
    PRIMARY KEY (id),
    FOREIGN KEY (id) REFERENCES person (id)
);

-- Sports Table --

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
    female_num INT,
    PRIMARY KEY (sport_code, id, year),
    FOREIGN KEY (id) REFERENCES person (id),
    FOREIGN KEY (sport_code) REFERENCES sport (sport_code)
);


CREATE TABLE event(
    sport_code VARCHAR(3),
    name VARCHAR(50),
    PRIMARY KEY (sport_code,name),
    FOREIGN KEY (sport_code) REFERENCES sport (sport_code)
);

--
CREATE TABLE medalists(
    sport_code VARCHAR(3),
    name VARCHAR(50),
    id INT,
    year INT,
    PRIMARY KEY (sport_code,name,id,year),
    FOREIGN KEY (sport_code, name) REFERENCES event (sport_code,name),
    FOREIGN KEY (id) REFERENCES person (id)
);
