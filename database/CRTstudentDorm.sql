DROP TABLE StudentDorm;

CREATE TABLE StudentDorm(
    netid varchar2(32),
    dorm varchar2(32),
    CONSTRAINT pkStudentDorm PRIMARY KEY (netid, dorm),
    CONSTRAINT fkDormNetid FOREIGN KEY (netid) REFERENCES Student(netid),
    CONSTRAINT fkDorm FOREIGN KEY (dorm) REFERENCES Dorm(dorm)
);
