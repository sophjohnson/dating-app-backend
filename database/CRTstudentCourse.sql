DROP TABLE StudentCourse;

CREATE TABLE StudentCourse(
    netid varchar2(32),
    course varchar2(32),
    CONSTRAINT pkStudentCourse PRIMARY KEY (netid, course),
    CONSTRAINT fkCourseNetid FOREIGN KEY (netid) REFERENCES Student(netid),
    CONSTRAINT fkCourseId FOREIGN KEY (course) REFERENCES Course(id)
);
