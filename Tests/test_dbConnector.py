from unittest import TestCase
import mysql.connector
import configparser
from KafkaRestServer.MySQLDB import dbConnector

__author__ = 'scotlov'


class TestDbConnector(TestCase):

    def getConnectionString(self):
        env = self.config['environment']['env']
        database = self.config[env]['database']
        host = self.config[env]['host']
        password = self.config[env]['password']
        user = self.config[env]['username']
        return mysql.connector.connect(user=user, password=password,host=host,database=database)

    def setUp(self):
        self.config  = configparser.ConfigParser()

        self.config.add_section('environment')
        self.config.set('environment','env','Test')

        self.config.add_section('Test')
        self.config.set('Test','query','SELECT word, count FROM words')
        self.config.set('Test','database','MessageStore')
        self.config.set('Test','host','localhost')
        self.config.set('Test','password','test')
        self.config.set('Test','username','test')

        # create dictionary of test words
        self.testWords = {'unitTest1':100,'unitTest2':100,'unitTest3':100,'unitTest4':100}

        self.insertTestWords(self.testWords)



    def insertTestWords(self,testWords):
        cnn = self.getConnectionString()
        cursor = cnn.cursor()

        #clean up db, removing any previous test runs
        cursor.execute("Delete From messagestore.words where word Like 'unitTest%'")
        cnn.commit()

        v =" "
        for key in testWords:
            a = key
            b = str(testWords[key])
            c = "(" + "\'" + a + "\'" + ',' + b + "),"
            v = v + c

        v =v[:-1]
        query = ("""INSERT INTO words values{0}""").format(v)
        cursor.execute(query)
        cnn.commit()


    def tearDown(self):
        cnn = self.getConnectionString()
        cursor = cnn.cursor()
        #restore db to original state
        query = ("""Delete From messagestore.words where word like'unitTest%'""")
        cursor.execute(query)
        cnn.commit()

    def test_readConfig(self):

        db = dbConnector(self.config)

        self.assertEqual(db.env,self.config.get('environment','env'))
        self.assertEqual(db.selectQuery,self.config.get('Test','query'))
        self.assertEqual(db.database,self.config.get('Test','database'))
        self.assertEqual(db.host,self.config.get('Test','host'))
        self.assertEqual(db.password,self.config.get('Test','password'))
        self.assertEqual(db.user,self.config.get('Test','username'))

    def test_getConnectionString(self):
        db = dbConnector(self.config)
        cnn = db.getConnectionString()
        database =    cnn.get_database()
        self.assertEqual(database,(self.config.get('Test','database')).lower())

    def test_getWordCounts(self):
        db = dbConnector(self.config)
        words = db.getWordCounts()

        for key in self.testWords:
            self.assertEqual(words[key],self.testWords[key])


