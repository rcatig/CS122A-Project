import mysql.connector
import sys
import csv
import mysql.connector

data_base = {
    "host": "localhost",
    "user": "test",
    "password": "password",
    "database": "cs122a"
}

TABLES = ["ModelConfigurations", "ModelServices", "LLMService", "DataStorage",
               "Configuration", "CustomizedModel", "Basemodel", "AgentClient",
               "AgentCreator", "InternetService", "User"]


DDLS = [ # hw2 solutions
    '''
    CREATE TABLE User (
        uid INT,
        email TEXT NOT NULL,
        username TEXT NOT NULL,
        PRIMARY KEY (uid)
    )
    ''',

    '''
    CREATE TABLE AgentCreator (
        uid INT,
        bio TEXT,
        payout TEXT,
        PRIMARY KEY (uid),
        FOREIGN KEY (uid) REFERENCES Users(uid) ON DELETE CASCADE
    )
    ''',

    '''
    CREATE TABLE AgentClient (
        uid INT,
        interests TEXT NOT NULL,
        cardholder TEXT NOT NULL,
        expire DATE NOT NULL,
        cardno INT NOT NULL,
        cvv INT NOT NULL,
        zip INT NOT NULL,
        PRIMARY KEY (uid),
        FOREIGN KEY (uid) REFERENCES Users(uid) ON DELETE CASCADE
    )
    ''',

    '''
    CREATE TABLE BaseModel (
        bmid INT,
        creator_uid INT NOT NULL,
        description TEXT NOT NULL,
        PRIMARY KEY (bmid),
        FOREIGN KEY (creator_uid) REFERENCES AgentCreator(uid) ON DELETE CASCADE
    )
    ''',

    '''
    CREATE TABLE CustomizedModel (
        bmid INT,
        mid INT NOT NULL,
        PRIMARY KEY (bmid, mid),
        FOREIGN KEY (bmid) REFERENCES BaseModel(bmid) ON DELETE CASCADE
    )
    ''',

    '''
    CREATE TABLE Configuration (
        cid INT,
        client_uid INT NOT NULL,
        content TEXT NOT NULL,
        labels TEXT NOT NULL,
        PRIMARY KEY (cid),
        FOREIGN KEY (client_uid) REFERENCES AgentClient(uid) ON DELETE CASCADE
    )
    ''',

    '''
    CREATE TABLE InternetService (
        sid INT,
        provider TEXT NOT NULL,
        endpoints TEXT NOT NULL,
        PRIMARY KEY (sid)
    )
    ''',

    '''
    CREATE TABLE LLMService (
        sid INT,
        domain TEXT,
        PRIMARY KEY (sid),
        FOREIGN KEY (sid) REFERENCES InternetService(sid) ON DELETE CASCADE
    )
    ''',

    '''
    CREATE TABLE DataStorage (
        sid INT,
        type TEXT,
        PRIMARY KEY (sid),
        FOREIGN KEY (sid) REFERENCES InternetService(sid) ON DELETE CASCADE
    )
    ''',

    '''
    CREATE TABLE ModelServices (
        bmid INT NOT NULL,
        sid INT NOT NULL,
        version INT NOT NULL,
        PRIMARY KEY (bmid, sid),
        FOREIGN KEY (bmid) REFERENCES BaseModel(bmid) ON DELETE CASCADE,
        FOREIGN KEY (sid) REFERENCES InternetService(sid) ON DELETE CASCADE
    )
    ''',

    '''
    CREATE TABLE ModelConfigurations (
        bmid INT NOT NULL,
        mid INT NOT NULL,
        cid INT NOT NULL,
        duration INT NOT NULL,
        PRIMARY KEY (bmid, mid, cid),
        FOREIGN KEY (bmid, mid) REFERENCES CustomizedModel(bmid, mid) ON DELETE CASCADE,
        FOREIGN KEY (cid) REFERENCES Configuration(cid) ON DELETE CASCADE
    )
    '''
]

INSERT_STATEMENTS = {
    "User": "INSERT INTO USER(uid,email,username) VALUES(%s,%s,%s)",
    "AgentCreator": "INSERT INTO AgentCreator(uid,bio,payout) VALUES(%s,%s,%s)",
    "AgentClient": "INSERT INTO AgentClient(uid,interests,cardholder,expire,cardno,cvv,zip) VALUES(%s,%s, %s, %s, %s, %s, %s)",
    "BaseModel": "INSERT INTO BaseModel(bmid,creator_uid,description) VALUES (%s,%s,%s)",
    "CustomizedModel": "INSERT INTO CustomizedModel(bmid,mid) VALUES (%s,%s)",
    "Configuration": "INSERT INTO Configuration(cid,client_uid,content,labels) VALUES (%s,%s,%s,%s)",
    "InternetService": "INSERT INTO InternetService(sid,provider,endpoints) VALUES (%s,%s,%s)",
    "LLMService": "INSERT INTO LLMService(sid,domain) VALUES (%s,%s)",
    "DataStorage": "INSERT INTO DataStorage(sid,type) VALUES (%s,%s)",
    "ModelServices": "INSERT INTO ModelServices(bmid,sid,version) VALUES (%s,%s,%s)",
    "ModelConfigurations": "INSERT INTO ModelConfigurations(bmid,mid,cid,duration) VALUES (%s,%s,%s,%s)"
}

def import_data(folderName):
    try:
        connec = connect_to_database()
        cursor = connec.cursor()

        # delete existing tables
        for table in TABLES:
            cursor.execute("DROP TABLE IF EXISTS " + table)

        # create new tables
        for statement in DDLS:
            cursor.execute(statement)

        # read the CSV files in given folder & import data into database
        for tableName in INSERT_STATEMENTS:
            filePath = folderName + "/" + tableName + ".csv"

            try:
                f = open(filePath, "r", encoding = "utf-8")
            except:
                continue

            # 1) read all lines in the file
            # 2) if there are no entries in the file, don't insert anything
            # 3) otherwise, parse it and insert into DB
            lines = f.readlines()
            f.close()

            if len(lines) <= 1:
                continue

            for line in lines[1:]:
                line = line.strip().split(",")
                line = [None if val == "NULL" else val for val in line]
                cursor.execute(INSERT_STATEMENTS[tableName], line)

        # save changes to DB, close connection, success msg
        connec.commit()
        cursor.close()
        connec.close()
        print("Success")
    except:
        print("Fail")


def connect_to_database():
    return mysql.connector.connect(data_base)


#def insertAgentClient():


#def addCustomizedModel():


#def deleteBaseModel():


#def listInternetService():


#def countCustomizedModel():


#def topNDurationConfig():


#def listBaseModelKeyWord():


#def printNL2SQLresult():


def main():
    function = sys.argv[1]
    arguments = sys.argv[2:]

    if function == "import":
        import_data(arguments)

if __name__ == '__main__':
    main()
