DROP TABLE Message;
DROP SEQUENCE seqMessage;

CREATE TABLE Message(
    messageID number,
    senderID varchar2(32),
    receiverID varchar2(32),
    content varchar2(256),
    timestamp date,
    CONSTRAINT pkMessage PRIMARY KEY (messageID),
    CONSTRAINT fkMessageSender FOREIGN KEY (senderID) REFERENCES Student(netid),
    CONSTRAINT fkMessageReceiver FOREIGN KEY (receiverID) REFERENCES Student(netid)
);

CREATE SEQUENCE seqMessage;

CREATE TRIGGER messageBeforeIns
BEFORE INSERT ON Message 
FOR EACH ROW
BEGIN
  SELECT seqMessage.nextval
  INTO :new.messageID
  FROM dual;
END;

/
