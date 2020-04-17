DROP TABLE Minor CASCADE CONSTRAINTS;

CREATE TABLE Minor(
    minor varchar2(64),
    CONSTRAINT pkMinor PRIMARY KEY (minor)
);
