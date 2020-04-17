DROP TABLE Preferences;

CREATE TABLE Preferences(
netid varchar2(32),
sexualOrientation varchar2(32),
genderIdentity varchar2(32),
mass varchar2(32),
dh varchar2(32),
fridayNights varchar2(32),
CONSTRAINT pkPreferences PRIMARY KEY (netid),
CONSTRAINT fkPreferencesStudent FOREIGN KEY (netid) REFERENCES Student(netid)
);
