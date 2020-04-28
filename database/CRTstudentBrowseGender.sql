DROP TABLE StudentBrowseGender;

CREATE TABLE StudentBrowseGender(
    netid varchar2(32),
    gender varchar2(32),
    CONSTRAINT pkStudentGender PRIMARY KEY (netid, gender),
    CONSTRAINT fkStudentGenderNetid FOREIGN KEY (netid) REFERENCES Student(netid),
    CONSTRAINT fkStudentGenderName FOREIGN KEY (gender) REFERENCES Gender(gender)
);
