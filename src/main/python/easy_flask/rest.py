"""
The module able to decorate code for service specification
"""
from easy_flask.exceptions import *


class Rest:
    __VERB = u'rest.Verb'
    __PATH = u'rest.Path'

    def __init__(self):
        self.__directives = {}

    # ------------------------------------------------------------------------

    def __decorate(self, key, value, exn):
        if key in self.__directives:
            raise exn()
        else:
            self.__directives[key] = value
            return lambda f: f

    # ------------------------------------------------------------------------

    def Path(self, path):
        return self.__decorate(Rest.__PATH, path, OverloadedPathException)

    def hasPath(self):
        return Rest.__PATH in self.__directives

    def getPath(self):
        if self.hasPath():
            return self.__directives[Rest.__PATH]
        else:
            return None

    # ------------------------------------------------------------------------

    def Verb(self, name):
        return self.__decorate(Rest.__VERB, name, OverloadedVerbException)

    def GET(self):
        return self.Verb('GET')

    def hasGET(self):
        return self.hasVerb('GET')

    def PUT(self):
        return self.Verb('PUT')

    def hasPUT(self):
        return self.hasVerb('PUT')

    def POST(self):
        return self.Verb('POST')

    def hasPOST(self):
        return self.hasVerb('POST')

    def DELETE(self):
        return self.Verb('DELETE')

    def hasDELETE(self):
        return self.hasVerb('DELETE')

    def hasVerb(self, verb):
        return Rest.__VERB in self.__directives and \
            self.__directives[Rest.__VERB] == verb
