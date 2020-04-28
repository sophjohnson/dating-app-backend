DROP TABLE Preferences;

CREATE TABLE Preferences(
    netid varchar2(32),
    temperament varchar2(32),
    giveAffection varchar2(32),
    trait varchar2(32),
    idealDate varchar2(32),
    fridayNight varchar2(32),
    diningHall varchar2(32),
    studySpot varchar2(32),
    mass varchar2(32),
    club varchar2(32),
    gameDay varchar2(32),
    hour varchar2(32),
    zodiacSign varchar2(32),
    idealTemperament varchar2(32),
    receiveAffection varchar2(32),
    idealTrait varchar2(32),
    CONSTRAINT pkPreferences PRIMARY KEY (netid),
    CONSTRAINT fkPreferencesStudent FOREIGN KEY (netid) REFERENCES Student(netid)
);
