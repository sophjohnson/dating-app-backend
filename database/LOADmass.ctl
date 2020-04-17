load data infile './csv/mass.csv'
insert into table mass 
fields terminated by "," optionally enclosed by '"'
(location,day,time)
