import cherrypy
from KafkaRestServer.MySQLDB import dbConnector


class Songs:

    exposed = True


    def GET(self):
        db = dbConnector('test','test','localhost','MessageStore')
        words = db.getWordCounts()

        output = []
        for k in words.keys():
            output.append(k + ':' +str(words[k]))

        return (', '.join(output))





if __name__ == '__main__':

    cherrypy.tree.mount(
        Songs(), '/api/songs',
        {'/':
            {'request.dispatch': cherrypy.dispatch.MethodDispatcher()}
        }
    )
    cherrypy.server.socket_port = 8083
    #cherrypy.server.httpserver = 'kafkaserver.cloudapp.net'
    cherrypy.server.socket_host = 'localhost'
    cherrypy.engine.start()
    cherrypy.engine.block()
