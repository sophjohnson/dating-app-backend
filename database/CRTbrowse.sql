DROP TABLE Browse;

CREATE TABLE Browse(
    viewedFor varchar2(32),
    netid varchar2(32),
    viewedBy varchar2(32),
    CONSTRAINT pkHistory PRIMARY KEY (viewedFor, netid, viewedBy),
    CONSTRAINT fkHistoryViewedFor FOREIGN KEY (viewedFor) REFERENCES Student(netid),
    CONSTRAINT fkHistoryNetid FOREIGN KEY (netid) REFERENCES Student(netid),
    CONSTRAINT fkHistoryViewedBy  FOREIGN KEY (viewedBy) REFERENCES Student(netid)
);
