DROP TABLE StudentMajor;

CREATE TABLE StudentMajor(
    netid varchar2(32),
    major varchar2(128),
    CONSTRAINT pkStudentMajor PRIMARY KEY (netid, major),
    CONSTRAINT fkStudentMajorNetid FOREIGN KEY (netid) REFERENCES Student(netid),
    CONSTRAINT fkStudentMajorName FOREIGN KEY (major) REFERENCES Major(major)
);
