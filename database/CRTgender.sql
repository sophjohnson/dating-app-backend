DROP TABLE Gender CASCADE CONSTRAINTS;

CREATE TABLE Gender(
    gender varchar2(32),
    CONSTRAINT pkGender PRIMARY KEY (gender)
);
