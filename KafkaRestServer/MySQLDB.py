import mysql.connector
import configparser
import logging


class dbConnector:

    def __init__(self):
        self.readConfig()


    def readConfig(self):
        config = configparser.ConfigParser()
        config.read('application.ini')

        env = config['environment']['env']

        self.user = config[env]['username']
        self.password = config[env]['password']
        self.host = config[env]['host']
        self.database = config[env]['database']
        self.selectQuery = config[env]['query']




    def getConnectionString(self):
        return(mysql.connector.connect(user=self.user, password=self.password,host=self.host,database=self.database))

    def getWordCounts(self):
        cnx = self.getConnectionString()
        cursor = cnx.cursor()
        #query = ("SELECT word, count FROM words")
        cursor.execute(self.selectQuery)

        words = {}
        for (word, count) in cursor:
            words[word]=count

        cursor.close()
        cnx.close()
        return words


db = dbConnector()
words = db.getWordCounts()

output = []
for k in words.keys():
    output.append(k + ':' +str(words[k]))

print (', '.join(output))


