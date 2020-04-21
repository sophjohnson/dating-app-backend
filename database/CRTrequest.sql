DROP TABLE Request;

CREATE TABLE Request(
    sender varchar2(32),
    receiver varchar2(32),
    status varchar2(16),
    timestamp date,
    CONSTRAINT pkRequest PRIMARY KEY (sender, receiver),
    CONSTRAINT fkRequestSender FOREIGN KEY (sender) REFERENCES Student(netid),
    CONSTRAINT fkRequestReceiver FOREIGN KEY (receiver) REFERENCES Student(netid)
);
