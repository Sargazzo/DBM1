-- If you insert athletes first ID = 1 did not win nothing
INSERT INTO enrolled VALUES('JUD',1,2028);
INSERT INTO enrolled VALUES('JUD',1,2024);

INSERT INTO medalists VALUES('JUD','Men -100 kg',1,'Gold', 2028);


INSERT INTO enrolled VALUES('ARC',1,2028);
INSERT INTO medalists VALUES('ARC','Men''s Individual - W1',1,'Gold', 2028);

SELECT * FROM medalists where id = 1;
SELECT * FROM enrolled where id = 1;

-- Test 7th query
INSERT INTO enrolled VALUES('WBK',8,2012);
INSERT INTO medalists VALUES('WBK','Women',8,'Gold', 2012);

INSERT INTO enrolled VALUES('ARC',8,2014);
INSERT INTO medalists VALUES('ARC','Women''s Individual - W1',8,'Gold', 2014);