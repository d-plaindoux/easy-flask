"""
Module providing specification capabilities using rest decorators.
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

    def combine(self, specification):
        if specification.hasPath():
            if self.hasPath():
                self.Path("%s/%s" % (specification.getPath(), self.getPath()))
            else:
                self.Path(specification.getPath())

        if specification.hasConsumes():
            [self.Consumes(c) for c in specification.getConsumes()]

        if specification.hasProduces():
            [self.Produces(c) for c in specification.getProduces()]

        return self

    # ------------------------------------------------------------------------
    # Private behaviors
    # ------------------------------------------------------------------------

    __VERB = u'rest@Verb'
    __PATH = u'rest@Path'
    __CONSUMES = u'rest@Consumes'
    __PRODUCES = u'rest@Produces'

    def __define(self, key, value, setup):
        """
        Register single specification
        """
        current = self.__specs[key] if key in self.__specs else None

        self.__specs[key] = setup(value, current=current)

        return lambda f: f

    @staticmethod
    def __filterByType(aType):
        """
        Determine the right filter selection depending on the input type
        """
        if aType is list:
            return lambda value, current: value in current
        else:
            return lambda value, current: value == current

    def __has(self, key, value):
        """
        Checker is a given key exists and the corresponding value is valid
        """
        if key in self.__specs:
            current = self.__specs[key]
            return self.__filterByType(type(current))(value, current)
        else:
            return False

    @staticmethod
    def __errorIfDefine(exn):
        """
        Method validating a value iff it does exist yet. Prohibits
        redefinition
        """

        def callback(value, current=None):
            if current is None:
                return value
            else:
                raise exn()

        return callback

    @staticmethod
    def __stackValues(value, current=None):
        """
        Method appending a value to a given list provided by current.
        """
        newCurrent = [] if current is None else list(current)

        if value not in newCurrent:
            newCurrent.append(value)

        return newCurrent

    # ------------------------------------------------------------------------
    # Path management
    # ------------------------------------------------------------------------

    def Path(self, path):
        """
        Define the rest URI as a Path. This path can contain typed variable
        definition. For this purpose the FLASK representation path is chosen.
        """
        return self.__define(self.__PATH, path,
                             self.__errorIfDefine(OverloadedPathException))

    def hasPath(self):
        """
        Check is a Path has been setup
        """
        return Specification.__PATH in self.__specs

    def getPath(self):
        """
        Returns the setup Path or None
        """
        if self.hasPath():
            return self.__specs[Specification.__PATH]
        else:
            return None

    # ------------------------------------------------------------------------
    # Verb management
    # ------------------------------------------------------------------------

    def Verb(self, name):
        """
        Define a verb like 'GET', 'PUT', 'POST', 'DELETE' and ...
        """
        return self.__define(self.__VERB, name,
                             self.__errorIfDefine(OverloadedVerbException))

    def hasVerb(self):
        """
        TODO
        """
        return Specification.__VERB in self.__specs

    def getVerb(self):
        """
        TODO
        """
        if self.hasVerb():
            return self.__specs[Specification.__VERB]
        else:
            return None

    def hasGivenVerb(self, verb):
        """
        TODO
        """
        return self.__has(Specification.__VERB, verb)

    # ------------------------------------------------------------------------
    # Consumes management
    # ------------------------------------------------------------------------

    def Consumes(self, mime):
        """
        TODO
        """
        return self.__define(self.__CONSUMES, mime, self.__stackValues)

    def hasConsumes(self):
        """
        TODO
        """
        return Specification.__CONSUMES in self.__specs

    def getConsumes(self):
        """
        TODO
        """
        if self.hasConsumes():
            return self.__specs[Specification.__CONSUMES]
        else:
            return None

    def hasGivenConsume(self, mime):
        """
        TODO
        """
        return self.__has(self.__CONSUMES, mime)

    # ------------------------------------------------------------------------
    # Produces management
    # ------------------------------------------------------------------------

    def Produces(self, mime):
        """
        TODO
        """
        return self.__define(self.__PRODUCES, mime, self.__stackValues)

    def hasProduces(self):
        """
        TODO
        """
        return Specification.__PRODUCES in self.__specs

    def getProduces(self):
        """
        TODO
        """
        if self.hasProduces():
            return self.__specs[Specification.__PRODUCES]
        else:
            return None

    def hasGivenProduce(self, mime):
        """
        TODO
        """
        return self.__has(self.__PRODUCES, mime)

    # ------------------------------------------------------------------------
    # Static behaviors
    # ------------------------------------------------------------------------

    @staticmethod
    def exists(function):
        """
        TODO
        """
        return "__rest__" in function.__dict__

    @staticmethod
    def get(function):
        """
        TODO
        """
        if "__rest__" not in function.__dict__:
            function.__dict__["__rest__"] = Specification()
        return function.__dict__["__rest__"]

    @staticmethod
    def getAndDefine(continuation):
        """
        TODO
        """

        def decorate(function):
            continuation(Specification.get(function))
            return function

        return decorate
