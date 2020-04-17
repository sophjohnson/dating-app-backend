DROP TABLE Dorm CASCADE CONSTRAINTS;

CREATE TABLE Dorm(
    dorm varchar2(32),
    mascot varchar2(16),
    quad varchar2(16),
    logo varchar2(16),
    airConditioning number,
    CONSTRAINT pkDorm PRIMARY KEY (dorm)
);
