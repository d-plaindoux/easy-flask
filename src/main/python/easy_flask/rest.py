"""
The module able to decorate code for service specification
"""
from easy_flask.exceptions import *


class Rest:
    def __init__(self):
        self.directives = {}

    def __decorate(self, key, value, exn):
        if key in self.directives:
            raise exn()
        else:
            self.directives[key] = value
            return lambda f: f

    def Path(self, path):
        __PATH = u'rest.Path'
        return self.__decorate(__PATH, path, OverloadedPathException)

    def Verb(self, name):
        __VERB = u'rest.Verb'
        return self.__decorate(__VERB, name, OverloadedVerbException)

    def GET(self):
        return self.Verb('GET')

    def PUT(self):
        return self.Verb('PUT')

    def POST(self):
        return self.Verb('POST')

    def DELETE(self):
        return self.Verb('DELETE')
