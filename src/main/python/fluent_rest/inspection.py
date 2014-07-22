"""
Inspection facility used to retrieve rest service specifications
"""

from inspect import getmembers
from inspect import isfunction
from inspect import isclass
from inspect import ismethod

from fluent_rest.rest import specs
from fluent_rest.rest import specsExists
from fluent_rest.exceptions import NotASuitableDefinitionException


class ClassInspector:
    """
    Inspector dedicated to a class definition
    """

    def __init__(self, clazz):
        self.clazz = clazz

    def __specInheritance(self, function):
        """
        Add class specification to the function specification if necessary
        """
        if specsExists(self.clazz):
            specs(function).combine(specs(self.clazz))

        return function

    def handle(self, handler):
        """
        Method used to identify specified functions in a given instance.
        Each function identified is handled using the parametric handler
        """
        functions = getmembers(self.clazz, predicate=ismethod)
        return [handler(self.__specInheritance(f)) for (_, f) in functions
                if specsExists(f)]


class FunctionInspector:
    """
    Inspector dedicated to function
    """

    def __init__(self, function):
        self.function = function

    def handle(self, handler):
        """
        Method used to identify specified functions in a given instance.
        Each function identified is handled using the parametric handler
        """
        functions = [self.function]
        return [handler(f) for f in functions if specsExists(f)]


def inspect(definition):
    """
    General inspection function which call the adapted inspector depending
    on the corresponding definition type: object of function.
    """
    if isclass(definition):
        return ClassInspector(definition)
    elif isfunction(definition):
        return FunctionInspector(definition)
    else:
        raise NotASuitableDefinitionException()
