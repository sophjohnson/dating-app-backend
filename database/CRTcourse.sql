DROP TABLE Course CASCADE CONSTRAINTS;

CREATE TABLE Course(
    crn number,
    name varchar2(64),
    CONSTRAINT pkCourse PRIMARY KEY (crn)
);
