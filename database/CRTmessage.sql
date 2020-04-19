DROP TABLE Message;
DROP SEQUENCE seqMessage;

CREATE TABLE Message(
    id number,
    conversation number,
    sender varchar2(32),
    receiver varchar2(32),
    content varchar2(256),
    timestamp date,
    CONSTRAINT pkMessage PRIMARY KEY (id),
    CONSTRAINT fkMessageSender FOREIGN KEY (sender) REFERENCES Student(netid),
    CONSTRAINT fkMessageReceiver FOREIGN KEY (receiver) REFERENCES Student(netid)
);

CREATE SEQUENCE seqMessage;

CREATE TRIGGER messageBeforeIns
BEFORE INSERT ON Message
FOR EACH ROW
BEGIN
  SELECT seqMessage.nextval
  INTO :new.id
  FROM dual;
END;

/
