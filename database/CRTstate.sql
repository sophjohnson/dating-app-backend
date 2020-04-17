DROP TABLE State CASCADE CONSTRAINTS;

CREATE TABLE State(
    code varchar2(2),
    state varchar2(32),
    CONSTRAINT pkState PRIMARY KEY (code)
);
