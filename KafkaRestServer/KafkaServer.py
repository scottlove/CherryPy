import cherrypy
import configparser
from KafkaRestServer.MySQLDB import dbConnector
import json
import logging

class wordCount():
    def __init__(self,word,count):
            self.name =word
            self.count= count;






class Words:

    def __init__(self,config):
        self.config = config

    exposed = True
    @cherrypy.tools.json_out()
    def GET(self):


        db = dbConnector(config)
        words = db.getWordCounts()

        output = []
        for k in words.keys():
            wo = {'word':k,'count':words[k]}
            output.append(wo)

        # return (', '.join(output))
        cherrypy.response.headers["Access-Control-Allow-Origin"] = "*"

        return(json.dumps(output))


def CORS():
    cherrypy.response.headers["Access-Control-Allow-Origin"] = "*"


if __name__ == '__main__':

    config = configparser.ConfigParser()
    config.read('application.ini')
    env = config['environment']['env']

    cherrypy.tree.mount(
        Words(config), '/api/words',
        {'/':
            {'request.dispatch': cherrypy.dispatch.MethodDispatcher()}
        }
    )


    cherrypy.server.socket_port = int(config[env]['port'])
    #cherrypy.server.httpserver = 'kafkaserver.cloudapp.net'
    cherrypy.server.socket_host = config[env]['host']
    cherrypy.tools.secureheaders = cherrypy.Tool('before_finalize',CORS,priority=60);



    cherrypy.engine.start()
    cherrypy.engine.block()
