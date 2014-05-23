import mysql.connector


class dbConnector:
    def __init__(self,user,password,host,database):
        self.user = user
        self.password = password
        self.host = host
        self.database = database

    def getConnectionString(self):
        return(mysql.connector.connect(user=self.user, password=self.password,host=self.host,database=self.database))

    def getWordCounts(self):
        cnx = self.getConnectionString()
        cursor = cnx.cursor()
        query = ("SELECT word, count FROM words")
        cursor.execute(query)

        words = {}
        for (word, count) in cursor:
            words[word]=count

        cursor.close()
        cnx.close()
        return words


db = dbConnector('test','test','localhost','MessageStore')
words = db.getWordCounts()

output = []
for k in words.keys():
    output.append(k + ':' +str(words[k]))

print (', '.join(output))


