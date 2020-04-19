DROP TABLE Conversation;
DROP SEQUENCE seqConversation;

CREATE TABLE Conversation(
    id number,
    student1 varchar2(32),
    student2 varchar2(32),
    CONSTRAINT pkConversation PRIMARY KEY (id),
    CONSTRAINT fkConversationStudent1 FOREIGN KEY (student1) REFERENCES Student(netid),
    CONSTRAINT fkConversationStudent2 FOREIGN KEY (student2) REFERENCES Student(netid)
);

CREATE SEQUENCE seqConversation;

CREATE TRIGGER conversationBeforeIns
BEFORE INSERT ON Conversation
FOR EACH ROW
BEGIN
  SELECT seqConversation.nextval
  INTO :new.id
  FROM dual;
END;

/
