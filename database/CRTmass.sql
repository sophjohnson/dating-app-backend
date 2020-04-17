DROP TABLE Mass CASCADE CONSTRAINTS;
DROP SEQUENCE seqMass;

CREATE TABLE Mass(
    massID number,
    location varchar2(128),
    day varchar2(32),
    time varchar2(16),
    CONSTRAINT pkMass PRIMARY KEY (massID)
);

CREATE SEQUENCE seqMass;

CREATE TRIGGER massBeforeIns
BEFORE INSERT ON Mass 
FOR EACH ROW
BEGIN
  SELECT seqMass.nextval
  INTO :new.massID
  FROM dual;
END;

/
