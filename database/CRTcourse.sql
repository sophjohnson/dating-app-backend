DROP TABLE Course CASCADE CONSTRAINTS;

CREATE TABLE Course(
    id varchar2(32),
    course varchar2(64),
    CONSTRAINT pkCourse PRIMARY KEY (id)
);
