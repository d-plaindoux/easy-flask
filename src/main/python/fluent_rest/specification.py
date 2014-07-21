"""
The specification
"""

from fluent_rest.exceptions import OverloadedPathException
from fluent_rest.exceptions import OverloadedVerbException


class Specification:
    """
    The specification class is able to manage REST oriented requirements for
    services definition in framework like flask
    """

    def __init__(self):
        self.__specs = {}

    # ------------------------------------------------------------------------
    # Private behaviors
    # ------------------------------------------------------------------------

    __VERB = u'rest@Verb'
    __PATH = u'rest@Path'
    __CONSUMES = u'rest@Consumes'
    __PRODUCES = u'rest@Produces'

    def __define(self, key, value, setup):
        current = self.__specs[key] if key in self.__specs else None

        self.__specs[key] = setup(value, current=current)

        return lambda f: f

    @staticmethod
    def __filterByType(aType):
        if aType is list:
            return lambda value, current: value in current
        else:
            return lambda value, current: value == current

    def __has(self, key, value):
        if key in self.__specs:
            current = self.__specs[key]
            return self.__filterByType(type(current))(value, current)
        else:
            return False

    @staticmethod
    def __errorIfDefine(exn):
        def callback(value, current=None):
            if current is None:
                return value
            else:
                raise exn()

        return callback

    @staticmethod
    def __stackValues(value, current=None):
        newCurrent = [] if current is None else list(current)

        if value not in newCurrent:
            newCurrent.append(value)

        return newCurrent

    # ------------------------------------------------------------------------
    # Path management
    # ------------------------------------------------------------------------

    def Path(self, path):
        return self.__define(self.__PATH, path,
                             self.__errorIfDefine(OverloadedPathException))

    def hasPath(self):
        return Specification.__PATH in self.__specs

    def getPath(self):
        if self.hasPath():
            return self.__specs[Specification.__PATH]
        else:
            return None

    # ------------------------------------------------------------------------
    # Verb management
    # ------------------------------------------------------------------------

    def Verb(self, name):
        return self.__define(self.__VERB, name,
                             self.__errorIfDefine(OverloadedVerbException))

    def hasVerb(self, verb):
        return self.__has(Specification.__VERB, verb)

    # ------------------------------------------------------------------------
    # Consumes management
    # ------------------------------------------------------------------------

    def Consumes(self, mime):
        return self.__define(self.__CONSUMES, mime, self.__stackValues)

    def hasConsumes(self, mime):
        return self.__has(self.__CONSUMES, mime)

    # ------------------------------------------------------------------------
    # Produces management
    # ------------------------------------------------------------------------

    def Produces(self, mime):
        return self.__define(self.__PRODUCES, mime, self.__stackValues)

    def hasProduces(self, mime):
        return self.__has(self.__PRODUCES, mime)

    # ------------------------------------------------------------------------
    # Static behaviors
    # ------------------------------------------------------------------------

    @staticmethod
    def exists(function):
        return "__rest__" in function.__dict__

    @staticmethod
    def get(function):
        if "__rest__" not in function.__dict__:
            function.__dict__["__rest__"] = Specification()
        return function.__dict__["__rest__"]

    @staticmethod
    def getAndDefine(continuation):
        def decorate(function):
            continuation(Specification.get(function))
            return function

        return decorate
