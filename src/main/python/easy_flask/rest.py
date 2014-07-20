"""
The module able to decorate code for service specification
"""
from easy_flask.exceptions import OverloadedPathException
from easy_flask.exceptions import OverloadedVerbException


class Rest:
    __VERB = u'rest.Verb'
    __PATH = u'rest.Path'

    def __init__(self):
        self.__spec = {}

    # ------------------------------------------------------------------------

    def __decorate(self, key, value, exn):
        if key in self.__spec:
            raise exn()
        else:
            self.__spec[key] = value
            return lambda f: f

    # ------------------------------------------------------------------------

    def Path(self, path):
        return self.__decorate(Rest.__PATH, path, OverloadedPathException)

    def hasPath(self):
        return Rest.__PATH in self.__spec

    def getPath(self):
        if self.hasPath():
            return self.__spec[Rest.__PATH]
        else:
            return None

    # ------------------------------------------------------------------------

    def Verb(self, name):
        return self.__decorate(Rest.__VERB, name, OverloadedVerbException)

    def hasVerb(self, verb):
        return Rest.__VERB in self.__spec and self.__spec[Rest.__VERB] == verb

#
# Module method
#


def __getRest(function):
    if "rest@Config" not in function.__dict__:
        function.__dict__["rest@Config"] = Rest()
    return function.__dict__["rest@Config"]


def __getRestAndApply(continuation):
    def decorate(function):
        continuation(__getRest(function))
        return function

    return decorate


def hasVerb(function, name):
    return __getRest(function).hasVerb(name)


def Verb(name):
    return __getRestAndApply(lambda s: s.Verb(name))


def hasGET(function):
    return hasVerb(function, 'GET')


GET = Verb('GET')


def hasPUT(function):
    return hasVerb(function, 'PUT')


PUT = Verb('PUT')


def hasPOST(function):
    return hasVerb(function, 'POST')


POST = Verb('POST')


def hasDELETE(function):
    return hasVerb(function, 'DELETE')


DELETE = Verb('DELETE')


def hasPath(function):
    return __getRest(function).hasPath()


def getPath(function):
    return __getRest(function).getPath()


def Path(path):
    return __getRestAndApply(lambda s: s.Path(path))
