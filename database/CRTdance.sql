DROP TABLE Dance;
DROP SEQUENCE seqDance;

CREATE TABLE Dance(
    danceID number,
    danceDate date,
    location varchar2(32),
    dorm varchar2(32),
    theme varchar2(64),
    CONSTRAINT pkDance PRIMARY KEY (danceID),
    CONSTRAINT fkDanceDorm FOREIGN KEY (dorm) REFERENCES Dorm(dorm)
);

CREATE SEQUENCE seqDance;

CREATE TRIGGER danceBeforeIns
BEFORE INSERT ON Dance 
FOR EACH ROW
BEGIN
  SELECT seqDance.nextval
  INTO :new.danceID
  FROM dual;
END;

/
