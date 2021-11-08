-- Some mockup data to satisfy some queries

-- IMPORTANT - TO USE THIS DATA RUN THE ATHLETES SCRIPT BEFORE RUNNING THE COACH ONE!!!! --

-- Test 7th query --

--One accomplish
INSERT INTO enrolled VALUES('WBK',8,2012);
INSERT INTO medalists VALUES('WBK','Women',8,'Gold', 2012);
INSERT INTO enrolled VALUES('ARC',8,2014);
INSERT INTO medalists VALUES('ARC','Women''s Individual - W1',8,'Gold', 2014);

-- Second accomplish
INSERT INTO person VALUES(10000,'Katha','RIKSTORY','AUT');
INSERT INTO athlete VALUES (10000,'10-10-1940','F');
INSERT INTO enrolled VALUES('ROW',10000,1960);
INSERT INTO medalists VALUES('ROW','PR3 Mixed Coxed Four - PR3Mix4+',10000,'Silver', 1960);
INSERT INTO enrolled VALUES('VBS',10000,1972);
INSERT INTO medalists VALUES('VBS','Women',10000,'Bronze', 1972);

-- Do not accomplish
INSERT INTO person VALUES(10001,'Klaus','MARTINEZ','BEN');
INSERT INTO athlete VALUES (10001,'10-11-1961','F');
INSERT INTO enrolled VALUES('VBS',10001,1976);
INSERT INTO medalists VALUES('VBS','Women',10001,'Silver', 1976);
INSERT INTO enrolled VALUES('VBS',10001,1980);
INSERT INTO medalists VALUES('VBS','Women',10001,'Gold', 1980);



-------- 8th query ----------

-- Accomplish
INSERT INTO enrolled VALUES('JUD',1,2028);
INSERT INTO medalists VALUES('JUD','Men -100 kg',1,'Gold', 2028);

--Accomplish
INSERT INTO person VALUES(20000,'Kevin','HEART','USA');
INSERT INTO athlete VALUES (20000,'5-11-1937','M');
INSERT INTO enrolled VALUES('VBS',20000,1976);
INSERT INTO enrolled VALUES('VBS',20000,1984);
INSERT INTO medalists VALUES('VBS','Men',20000,'Gold', 1984);

-- Accomplish
INSERT INTO person VALUES(20006,'Jingle','BELL','GER');
INSERT INTO athlete VALUES (20006,'5-11-1888','F');
INSERT INTO enrolled VALUES('WBK',20006,1908);
INSERT INTO enrolled VALUES('WBK',20006,1916);
INSERT INTO medalists VALUES('WBK','Women',20006,'Silver', 1916);

-- Do not accomplish

INSERT INTO person VALUES(20001,'Last','CHRISTMAS','CAM');
INSERT INTO athlete VALUES (20001,'5-11-1986','M');
INSERT INTO enrolled VALUES('VBS',20001,2000);
INSERT INTO enrolled VALUES('VBS',20001,2004);
INSERT INTO enrolled VALUES('VBS',20001,2008);
INSERT INTO medalists VALUES('VBS','Men',20001,'Gold', 2008);