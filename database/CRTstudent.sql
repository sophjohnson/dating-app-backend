DROP TABLE Student CASCADE CONSTRAINTS;

CREATE TABLE Student(
    netid varchar2(32),
    firstName varchar2(64),
    lastName varchar2(64),
    classYear varchar2(32),
    city varchar2(32),
    state varchar2(2),
    dorm varchar2(32),
    password varchar2(256),
    CONSTRAINT pkStudent PRIMARY KEY (netid),
    CONSTRAINT fkStudentState FOREIGN KEY (state) REFERENCES State(code),
    CONSTRAINT fkStudentDorm FOREIGN KEY (dorm) REFERENCES Dorm(dorm)
);
