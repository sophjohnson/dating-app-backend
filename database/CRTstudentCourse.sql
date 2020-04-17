DROP TABLE StudentCourse;

CREATE TABLE StudentCourse(
    netid varchar2(32),
    crn number,
    CONSTRAINT pkStudentCourse PRIMARY KEY (netid, crn),
    CONSTRAINT fkCourseNetid FOREIGN KEY (netid) REFERENCES Student(netid),
    CONSTRAINT fkCourseCRN FOREIGN KEY (crn) REFERENCES Course(crn)
);
