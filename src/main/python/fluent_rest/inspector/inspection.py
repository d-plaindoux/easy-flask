"""
Inspection facility used to retrieve rest service specifications
"""

from inspect import getmembers
from inspect import isfunction
from inspect import isclass
from inspect import ismethod

from fluent_rest.spec.rest import specs
from fluent_rest.spec.rest import specsExists
from fluent_rest.exceptions import NotASuitableDefinitionException


class Inspector:
    """
    Abstract class dedicated to entity (function, class or instance)
    inspection
    """

    def __init__(self, entries):
        self.entries = entries

    def inherits(self, function):
        raise Exception("Not Implemented")

    def performClosure(self):
        """
        Method used to identify specified functions in a given instance.
        """
        return [self.inherits(f) for f in self.entries if specsExists(f)]

    def handle(self, handler):
        """
        Method used to identify specified functions in a given instance.
        Each function identified is handled using the parametric handler
        """
        return [handler(f) for f in self.entries if specsExists(f)]

class ObjectInspector(Inspector):
    """
    Inspector dedicated to a class definition
    """

    def __init__(self, container, clazz):
        Inspector.__init__(self, ObjectInspector.__methods(container))
        self.container = container
        self.clazz = clazz
        self.performClosure()

    def inherits(self, function):
        """
        Add class specification to the function specification if necessary
        """
        if specsExists(self.clazz):
            specs(function).combine(specs(self.clazz))

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
        self.performClosure()

    def inherits(self, function):
        return function


def inspect(definition):
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