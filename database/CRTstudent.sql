DROP TABLE Student CASCADE CONSTRAINTS;

CREATE TABLE Student(
    netid varchar2(16),
    password varchar2(256),
    firstName varchar2(32),
    lastName varchar2(32),
    gradYear varchar2(4),
    city varchar2(32),
    state varchar2(2),
    dorm varchar2(32),
    orientation varchar2(32),
    identity varchar2(32),
    CONSTRAINT pkStudent PRIMARY KEY (netid),
    CONSTRAINT fkStudentState FOREIGN KEY (state) REFERENCES State(code),
    CONSTRAINT fkStudentDorm FOREIGN KEY (dorm) REFERENCES Dorm(dorm)
);
