DROP TABLE StudentMinor;

CREATE TABLE StudentMinor(
    netid varchar2(32),
    minor varchar2(128),
    CONSTRAINT pkStudentMinor PRIMARY KEY (netid, minor),
    CONSTRAINT fkStudentMinorNetid FOREIGN KEY (netid) REFERENCES Student(netid),
    CONSTRAINT fkStudentMinorName FOREIGN KEY (minor) REFERENCES Minor(minor)
);
