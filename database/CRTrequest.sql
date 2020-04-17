DROP TABLE Request;

CREATE TABLE Request(
    senderID varchar2(32),
    receiverID varchar2(32),
    status varchar2(16),
    CONSTRAINT pkRequest PRIMARY KEY (senderID, receiverID),
    CONSTRAINT fkRequestSender FOREIGN KEY (senderID) REFERENCES Student(netid),
    CONSTRAINT fkRequestReceiver FOREIGN KEY (receiverID) REFERENCES Student(netid)
);
