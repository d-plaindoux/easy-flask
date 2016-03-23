# Copyright (C)2015 D. Plaindoux.
#
# This program is free software; you can redistribute it and/or modify it
# under the terms of the GNU Lesser General Public License as published by
# the Free Software Foundation; either version 2, or (at your option) any
# later version.

from inspect import getmembers
from inspect import isfunction
from inspect import isclass
from inspect import ismethod

from abc import abstractmethod
from fluent_rest.spec.rest import specification
from fluent_rest.spec.rest import specificationExists
from fluent_rest.exceptions import NotASuitableDefinitionException


class Inspector:
    """
    Abstract class dedicated to entity (function, class or instance)
    inspection
    """

    def __init__(self, entries):
        self.entries = entries

    @abstractmethod
    def inherits(self, function):
        pass

    def transitiveClosure(self):
        """
        Method used to identify specified functions in a given instance.
        """
        return [self.inherits(f) for f in self.entries if
                specificationExists(f)]

    def handle(self, handler):
        """
        Method used to identify specified functions in a given instance.
        Each function identified is handled using the parametric handler
        """
        return [handler(f) for f in self.entries if specificationExists(f)]


class ObjectInspector(Inspector):
    """
    Inspector dedicated to a class definition
    """

    def __init__(self, element, clazz):
        Inspector.__init__(self, ObjectInspector.__methods(element))
        self.container = element
        self.clazz = clazz
        self.transitiveClosure()

    def inherits(self, function):
        """
        Add class specification to the function specification if necessary
        """
        if specificationExists(self.clazz):
            specification(function).combine(specification(self.clazz))

        return function

    @staticmethod
    def __methods(container):
        return [f for (_, f) in getmembers(container, predicate=ismethod)]


class FunctionInspector(Inspector):
    """
    Inspector dedicated to function
    """

    def __init__(self, function):
        Inspector.__init__(self, [function])
        self.transitiveClosure()

    def inherits(self, function):
        return function


def inspector(definition):
    """
    General inspection function which call the adapted inspector depending
    on the corresponding definition type: object of function.
    """
    if isclass(definition):
        return ObjectInspector(definition, definition)
    elif isfunction(definition):
        return FunctionInspector(definition)
    elif isinstance(definition, object):
        return ObjectInspector(definition, definition.__class__)
    else:
        raise NotASuitableDefinitionException()
