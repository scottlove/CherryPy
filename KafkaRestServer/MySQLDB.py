import mysql.connector
import configparser
import logging


class dbConnector:

    def __init__(self,config):

        self.env = config['environment']['env']
        self.selectQuery = config[self.env]['query']
        self.database = config[self.env]['database']
        self.host = config[self.env]['host']
        self.password = config[self.env]['password']
        self.user = config[self.env]['username']




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





