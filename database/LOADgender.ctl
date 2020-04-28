load data infile './csv/gender.csv'
insert into table gender 
fields terminated by "," optionally enclosed by '"'
(gender)
