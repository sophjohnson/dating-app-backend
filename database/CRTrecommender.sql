DROP TABLE Recommender;

CREATE TABLE Recommender(
    recommenderID varchar2(32),
    recommendeeID varchar2(32),
    CONSTRAINT pkRecommender PRIMARY KEY (recommenderID, recommendeeID),
    CONSTRAINT fkRecommender FOREIGN KEY (recommenderID) REFERENCES Student(netid),
    CONSTRAINT fkRecommendee FOREIGN KEY (recommendeeID) REFERENCES Student(netid)
);
