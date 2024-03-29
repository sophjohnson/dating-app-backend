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
    identity varchar2(32),
    question varchar2(64),
    image varchar2(32),
    danceInvite number,
    CONSTRAINT pkStudent PRIMARY KEY (netid),
    CONSTRAINT fkStudentState FOREIGN KEY (state) REFERENCES State(code),
    CONSTRAINT fkStudentDorm FOREIGN KEY (dorm) REFERENCES Dorm(dorm),
    CONSTRAINT fkStudentGender FOREIGN KEY (identity) REFERENCES Gender(gender)
);
