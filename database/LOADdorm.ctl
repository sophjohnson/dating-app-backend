load data infile './csv/dorm.csv'
insert into table dorm 
fields terminated by "," optionally enclosed by '"'
(dorm, quad, mascot, airConditioning)
