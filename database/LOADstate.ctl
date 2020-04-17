load data infile './csv/state.csv'
insert into table state 
fields terminated by "," optionally enclosed by '"'
(state,code)
