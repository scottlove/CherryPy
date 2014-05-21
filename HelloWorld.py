"""This example can handle the URIs
/    -> OnePage.index
/foo -> OnePage.foo -> foo
"""
import cherrypy


class OnePage(object):
    def index(self):
        return "one page!"
    index.exposed = True


def foo():
    return 'Foo!'
foo.exposed = True

if __name__ == '__main__':
    root = OnePage()
    root.foo = foo
    cherrypy.quickstart(root)