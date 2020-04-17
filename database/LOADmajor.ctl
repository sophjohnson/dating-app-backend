load data infile './csv/major.csv'
insert into table major 
fields terminated by "," optionally enclosed by '"'
(major)
