DROP TABLE Lunch;
DROP SEQUENCE seqLunch;

CREATE TABLE Lunch(
    id integer,
    netid varchar2(32),
    day varchar2(2),
    startTime date,
    endTime date,
    CONSTRAINT pkLunch PRIMARY KEY (netid, day, startTime),
    CONSTRAINT fkLunchNetid FOREIGN KEY (netid) REFERENCES Student(netid)
);

CREATE SEQUENCE seqLunch;

CREATE TRIGGER lunchBeforeIns
BEFORE INSERT ON Lunch
FOR EACH ROW
BEGIN
  SELECT seqLunch.nextval
  INTO :new.id
  FROM dual;
END;

/
