# Copyright (C)2016 D. Plaindoux.
#
# This program is free software; you can redistribute it and/or modify it
# under the terms of the GNU Lesser General Public License as published by
# the Free Software Foundation; either version 2, or (at your option) any
# later version.

from fluent_rest.exceptions import OverloadedPathException
from fluent_rest.exceptions import OverloadedProducerException
from fluent_rest.exceptions import OverloadedProviderException
from fluent_rest.exceptions import OverloadedVerbException


class Specification:
    """
    The specification class is able to manage REST oriented requirements for
    services definition in framework like flask
    """

    def __init__(self):
        self.__inherited = None
        self.__specs = {}

    def combine(self, specification):
        self.__inherited = specification
        return self

    def __str__(self):
        return str(self.__specs)

    # ------------------------------------------------------------------------
    # Private behaviors
    # ------------------------------------------------------------------------

    __VERB = u'rest@Verb'
    __PATH = u'rest@Path'
    __CONSUMES = u'rest@Consumes'
    __PRODUCES = u'rest@Produces'
    __PROVIDER = u'rest@Provider'

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
        return self.__define(self.__PATH,
                             path,
                             self.__errorIfDefine(OverloadedPathException))

    def hasPath(self):
        """
        Check is a Path has been setup
        """
        return (
            Specification.__PATH in self.__specs
            or
            (
                not self.__inherited is None
                and
                self.__inherited.hasPath()
            )
        )

    def getPath(self):
        """
        Returns the setup Path or None
        """

        def combinedPath():
            if self.__inherited and self.__inherited.hasPath():
                c = self.__inherited.getPath()
                return lambda p: "%s/%s" % (c, p) if p else c
            else:
                return lambda p: p

        def localPath():
            if Specification.__PATH in self.__specs:
                return self.__specs[Specification.__PATH]
            else:
                return None

        if self.hasPath():
            return combinedPath()(localPath())
        else:
            return None

    # ------------------------------------------------------------------------
    # Verb management
    # ------------------------------------------------------------------------

    def Verb(self, name):
        """
        Define a verb like 'GET', 'PUT', 'POST', 'DELETE' and ...
        """
        return self.__define(self.__VERB,
                             name,
                             self.__errorIfDefine(OverloadedVerbException))

    def hasVerb(self):
        """
        Check if a verb already exists
        """
        return Specification.__VERB in self.__specs

    def getVerb(self):
        """
        Retrieve the defined verb. If it does not exist it returns None
        """
        if self.hasVerb():
            return self.__specs[Specification.__VERB]
        else:
            return None

    def hasGivenVerb(self, verb):
        """
        Check if a given verb already exists
        """
        return (
            self.__has(self.__VERB, verb)
            or
            (
                not self.__inherited is None
                and
                self.__inherited.hasGivenVerb(verb)
            )
        )

    # ------------------------------------------------------------------------
    # Consumes management
    # ------------------------------------------------------------------------

    def Consumes(self, mime, transducer=None):
        """
        TODO
        """
        if transducer:
            self.__define(self.__CONSUMES + "@" + mime,
                          transducer,
                          self.__stackValues)

        return self.__define(self.__CONSUMES, mime, self.__stackValues)

    def hasConsumes(self):
        """
        TODO
        """
        return (
            Specification.__CONSUMES in self.__specs
            or
            (
                not self.__inherited is None
                and
                self.__inherited.hasConsumes(self)
            )
        )

    def hasGivenConsumes(self, mime):
        """
        TODO
        """
        return (
            self.__has(self.__CONSUMES, mime)
            or
            (
                not self.__inherited is None
                and
                self.__inherited.hasGivenConsumes(mime)
            )
        )

    # ------------------------------------------------------------------------
    # Produces management
    # ------------------------------------------------------------------------

    def Produces(self, mime, transducer=None):
        """
        TODO
        """
        if transducer:
            self.__define(self.__PRODUCES + "@" + mime,
                          transducer,
                          self.__errorIfDefine(OverloadedProducerException))

        return self.__define(self.__PRODUCES, mime, self.__stackValues)

    def hasProduces(self):
        """
        TODO
        """
        return (
            Specification.__PRODUCES in self.__specs
            or
            (
                not self.__inherited is None
                and
                self.__inherited.hasProduced()
            )
        )

    def getGivenProduces(self, mime):
        if Specification.__PRODUCES + "@" + mime in self.__specs:
            return self.__specs[Specification.__PRODUCES + "@" + mime]

        if not self.__inherited is None:
            return self.__inherited.getGivenProduces(mime)

        return lambda e: e

    def hasGivenProduces(self, mime):
        """
        TODO
        """
        return (
            self.__has(self.__PRODUCES, mime)
            or
            (
                not self.__inherited is None
                and
                self.__inherited.hasGivenProduces(mime)
            )
        )

    # ------------------------------------------------------------------------
    # Providers management
    # ------------------------------------------------------------------------

    def Provider(self, aType):
        """
        TODO
        """
        return self.__define(self.__PROVIDER,
                             aType,
                             self.__errorIfDefine(OverloadedProviderException))

    def hasProvider(self):
        """
        TODO
        """
        return (
            Specification.__PROVIDER in self.__specs
            or
            (
                not self.__inherited is None
                and
                self.__inherited.hasProvider()
            )
        )

    def getProvider(self):
        """
        Retrieve the defined provider. If it does not exist it returns None
        """
        if self.hasProvider():
            return self.__specs[Specification.__PROVIDER]
        else:
            return None

    def hasGivenProvider(self, type):
        """
        TODO
        """
        return (
            self.__has(self.__PROVIDER, type)
            or
            (
                not self.__inherited is None
                and
                self.__inherited.hasGivenProvider(type)
            )
        )

    # ------------------------------------------------------------------------
    # Static behaviors
    # ------------------------------------------------------------------------

    @staticmethod
    def exists(element):
        """
        Check whether an element has an attached REST specification
        """
        return hasattr(element, 'rest_specification')

    @staticmethod
    def get(element):
        """
        Method called when a specification must be retrieved. If no one exists
        a fresh specification is generated and attached to the parametric
        element
        """
        if not Specification.exists(element):
            # TODO(didier) Find a better solution for rest spec' injection
            element.rest_specification = Specification()
        return element.rest_specification
