DROP TABLE Major CASCADE CONSTRAINTS;

CREATE TABLE Major(
    major varchar2(64),
    CONSTRAINT pkMajor PRIMARY KEY (major)
);
