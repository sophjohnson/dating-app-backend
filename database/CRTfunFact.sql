DROP TABLE FunFact CASCADE CONSTRAINTS;
DROP SEQUENCE seqFunFact;

CREATE TABLE FunFact(
    id number,
    netid varchar2(32),
    caption varchar2(256),
    photo varchar2(32),
    CONSTRAINT pkFunFact PRIMARY KEY (id),
    CONSTRAINT fkFunFactNetid FOREIGN KEY (netid) REFERENCES Student(netid)
);

CREATE SEQUENCE seqFunFact;

CREATE TRIGGER funFactBeforeIns
BEFORE INSERT ON FunFact
FOR EACH ROW
BEGIN
  SELECT seqFunFact.nextval
  INTO :new.id
  FROM dual;
END;

/
