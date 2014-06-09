import cherrypy
import configparser
from KafkaRestServer.MySQLDB import dbConnector
import json
import logging


class Words:



    exposed = True
    #cherrypy.tools.json_out()
    def GET(self):

        db = dbConnector()
        words = db.getWordCounts()

        output = []
        for k in words.keys():
            output.append(k + ':' +str(words[k]))

        # return (', '.join(output))
        return(json.dumps(words))


if __name__ == '__main__':

    cherrypy.tree.mount(
        Words(), '/api/words',
        {'/':
            {'request.dispatch': cherrypy.dispatch.MethodDispatcher()}
        }
    )


    config = configparser.ConfigParser()
    config.read('application.ini')
    env = config['environment']['env']

    cherrypy.server.socket_port = int(config[env]['port'])
    #cherrypy.server.httpserver = 'kafkaserver.cloudapp.net'
    cherrypy.server.socket_host = config[env]['host']

    cherrypy.engine.start()
    cherrypy.engine.block()
