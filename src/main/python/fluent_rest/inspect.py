"""
Inspection facility used to retrieve rest service specifications
"""

from inspect import getmembers
from inspect import ismethod
from fluent_rest.rest import specExists


class ClassInspector:
    def __init__(self, instance, handler):
        self.instance = instance
        self.handler = handler

    def routes(self):
        """
        Method used to identify specified functions in a given instance.
        Each function identified is handled using the parametric handler
        """
        functions = getmembers(self.instance, predicate=ismethod)
        return [self.handler(f) for (_, f) in functions if specExists(f)]

