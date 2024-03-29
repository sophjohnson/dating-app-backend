DROP TABLE Recommendation;

CREATE TABLE Recommendation(
    viewer varchar2(32),
    viewee varchar2(32),
    status varchar2(32),
    recommendedBy varchar2(32),
    timestamp date,
    CONSTRAINT pkRecommendation PRIMARY KEY (viewer, viewee),
    CONSTRAINT fkViewer FOREIGN KEY (viewer) REFERENCES Student(netid),
    CONSTRAINT fkOption FOREIGN KEY (viewee) REFERENCES Student(netid),
    CONSTRAINT fkRecommendedBy FOREIGN KEY (recommendedBy) REFERENCES Student(netid)
);
