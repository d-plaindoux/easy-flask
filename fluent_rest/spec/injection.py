# Copyright (C)2014 D. Plaindoux.
#
# This program is free software; you can redistribute it and/or modify it
# under the terms of the GNU Lesser General Public License as published by
# the Free Software Foundation; either version 2, or (at your option) any
# later version.

import inspect
from fluent_rest.exceptions import NotASuitableDefinitionException


class ClassProvider:
    def __init__(self, model):
        self.model = model


class InstanceProvider:
    def __init__(self, instance):
        self.instance = instance


class ClassMethodProvider:
    def __init__(self, method):
        self.method = method


class InstanceMethodProvider:
    def __init__(self, method):
        self.method = method


class FunctionProvider:
    def __init__(self, function):
        self.function = function


class Binder:
    def __init__(self, aType, aProvider):
        self.aType = aType
        if inspect.isclass(aProvider):
            self.aProvider = ClassProvider(aProvider)
        elif inspect.isfunction(aProvider):
            self.aProvider = FunctionProvider(aProvider)
        elif inspect.ismethod(aProvider):
            if aProvider.__self__:
                self.aProvider = InstanceMethodProvider(aProvider)
            else:
                self.aProvider = ClassMethodProvider(aProvider)
        elif isinstance(aProvider, aType):
            self.aProvider = InstanceProvider(aProvider)
        else:
            raise NotASuitableDefinitionException()

    def accept(self, aType):
        return self.aType is aType

    def provider(self):
        return self.aProvider


class Injection:
    def __init__(self):
        self.binders = []

    def bind(self, aType, aProvider):
        self.binders.append(Binder(aType, aProvider))
        return self

    def accept(self, aType):
        try:
            return (b for b in self.binders if b.accept(aType)).next()
        except StopIteration:
            return None

    def provide(self, aType):
        pass

