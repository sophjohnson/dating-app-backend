DROP TABLE Recommender;

CREATE TABLE Recommender(
    recommender varchar2(32),
    recommendee varchar2(32),
    CONSTRAINT pkRecommender PRIMARY KEY (recommender, recommendee),
    CONSTRAINT fkRecommender FOREIGN KEY (recommender) REFERENCES Student(netid),
    CONSTRAINT fkRecommendee FOREIGN KEY (recommendee) REFERENCES Student(netid)
);
