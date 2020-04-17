DROP TABLE Lunch;

CREATE TABLE Lunch(
    netid varchar2(32),
    day varchar2(32),
    startTime varchar2(32),
    endTime varchar2(32),
    CONSTRAINT pkLunch PRIMARY KEY (netid, day),
    CONSTRAINT fkLunchNetid FOREIGN KEY (netid) REFERENCES Student(netid)
);
