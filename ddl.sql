DROP TABLE IF EXISTS ModelServices;
DROP TABLE IF EXISTS ModelConfigurations;
DROP TABLE IF EXISTS Configuration;
DROP TABLE IF EXISTS CustomizedModel;
DROP TABLE IF EXISTS BaseModel;
DROP TABLE IF EXISTS AgentCreator;
DROP TABLE IF EXISTS AgentClient;
DROP TABLE IF EXISTS User;
DROP TABLE IF EXISTS LLMService;
DROP TABLE IF EXISTS DataStorage;
DROP TABLE IF EXISTS InternetService;



CREATE TABLE User (
    uid INT PRIMARY KEY,
    email VARCHAR(100) NOT NULL,
    username VARCHAR(50) NOT NULL
);

CREATE TABLE AgentCreator (
    uid INT PRIMARY KEY,
    bio VARCHAR(255),
    payout VARCHAR(100) NOT NULL,
    FOREIGN KEY (uid) REFERENCES User(uid)
        ON DELETE CASCADE ON UPDATE CASCADE
);

CREATE TABLE AgentClient (
    uid INT PRIMARY KEY,
    interests VARCHAR(255),
    cardholder VARCHAR(50) NOT NULL,
    expire DATE NOT NULL,
    cardno BIGINT NOT NULL,
    cvv INT NOT NULL,
    zip INT NOT NULL,
    FOREIGN KEY (uid) REFERENCES User(uid)
        ON DELETE CASCADE ON UPDATE CASCADE
);


CREATE TABLE BaseModel (
    bmid INT NOT NULL,
    creator_uid INT NOT NULL,
    description VARCHAR(255),
    PRIMARY KEY(BMID),
    FOREIGN KEY(creator_uid) REFERENCES AgentCreator(UID)
                       ON DELETE NO ACTION

);

CREATE TABLE CustomizedModel (
    bmid INT,
    mid INT,
    PRIMARY KEY(bmid, mid),
    FOREIGN KEY(bmid) REFERENCES BaseModel(bmid)
                             ON DELETE CASCADE
);

CREATE TABLE InternetService (
    sid INT PRIMARY KEY,
    provider VARCHAR(255) NOT NULL,
    endpoints VARCHAR(255)
);

CREATE TABLE LLMService (
    sid INT PRIMARY KEY,
    domain VARCHAR(255) NOT NULL,
    FOREIGN KEY(sid) REFERENCES InternetService(sid)
                        ON DELETE CASCADE
);

CREATE TABLE Configuration (
    cid INT PRIMARY KEY,
    client_uid INT NOT NULL,
    content VARCHAR(255),
    labels VARCHAR(255),
    FOREIGN KEY(client_uid) REFERENCES AgentClient(uid)
                           ON DELETE CASCADE
);

CREATE TABLE DataStorage (
    sid INT PRIMARY KEY,
    type VARCHAR(255) NOT NULL,
    FOREIGN KEY(sid) REFERENCES InternetService(sid)
                         ON DELETE CASCADE
);

CREATE TABLE ModelServices (
    bmid INT NOT NULL,
    sid INT NOT NULL,
    version INT NOT NULL,
    PRIMARY KEY(bmid, sid),
    FOREIGN KEY(bmid) REFERENCES BaseModel(bmid)
                           ON DELETE CASCADE,
    FOREIGN KEY(sid) REFERENCES InternetService(sid)
                           ON DELETE CASCADE

);

CREATE TABLE ModelConfigurations (
    bmid INT NOT NULL,
    mid INT NOT NULL,
    cid INT NOT NULL,
    duration INT NOT NULL,
    PRIMARY KEY(bmid, mid, cid),
    FOREIGN KEY(cid) REFERENCES Configuration(cid)
                                 ON DELETE CASCADE,
    FOREIGN KEY(bmid, mid) REFERENCES CustomizedModel(bmid,mid)
                                 ON DELETE CASCADE
);
