import cherrypy
import configparser
from KafkaRestServer.MySQLDB import dbConnector
import json
import logging

class wordCount:
    def __init__(self,word,count):
            self.name =word
            self.count= count;



class Words:

    exposed = True
    @cherrypy.tools.json_out()
    def GET(self):


        db = dbConnector()
        words = db.getWordCounts()

        output = []
        for k in words.keys():
            output.append(k + ':' +str(words[k]))

        # return (', '.join(output))
        cherrypy.response.headers["Access-Control-Allow-Origin"] = "*";
        i = wordCount("test",1)
        # return(json.dumps(words))
        return(i)

def CORS():
    cherrypy.response.headers["Access-Control-Allow-Origin"] = "*"


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
    cherrypy.tools.secureheaders = cherrypy.Tool('before_finalize',CORS,priority=60);



    cherrypy.engine.start()
    cherrypy.engine.block()
