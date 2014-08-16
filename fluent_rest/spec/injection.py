# Copyright (C)2014 D. Plaindoux.
#
# This program is free software; you can redistribute it and/or modify it
# under the terms of the GNU Lesser General Public License as published by
# the Free Software Foundation; either version 2, or (at your option) any
# later version.

import inspect
from abc import abstractmethod
from fluent_rest.exceptions import NotASuitableDefinitionException


class Provider:
    def __init__(self):
        pass

    @abstractmethod
    def get(self, _):
        return None


class ClassProvider(Provider):
    def __init__(self, model):
        Provider.__init__(self)
        self.model = model

    def get(self, injection):
        return injection.model(self.model)


class InstanceProvider(Provider):
    def __init__(self, instance):
        Provider.__init__(self)
        self.instance = instance

    def get(self, injection):
        return injection.instance(self.instance)


class ClassMethodProvider(Provider):
    def __init__(self, method):
        Provider.__init__(self)
        self.method = method

    def get(self, injection):
        return injection.method(self.method)


class InstanceMethodProvider(Provider):
    def __init__(self, method):
        Provider.__init__(self)
        self.method = method

    def get(self, injection):
        return injection.function(self.method)


class FunctionProvider(Provider):
    def __init__(self, function):
        Provider.__init__(self)
        self.function = function

    def get(self, injection):
        return injection.function(self.function)


class Binder:
    def __init__(self, aType, aProvider):
        self.aType = aType
        if inspect.isclass(aProvider):
            self.aProvider = ClassProvider(aProvider)
        elif inspect.isfunction(aProvider):
            self.aProvider = FunctionProvider(aProvider)
        elif inspect.ismethod(aProvider) and aProvider.__self__:
            self.aProvider = InstanceMethodProvider(aProvider)
        elif inspect.ismethod(aProvider) and not aProvider.__self__:
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

    def closure(self, instance):
        return instance

    def model(self, model):
        return self.closure(model())

    def instance(self, instance):
        return self.closure(instance)

    def method(self, method):
        instance = self.closure(self.model(method.im_class()))
        return self.closure(method(instance))

    def function(self, method):
        return self.closure(method())

    def accept(self, aType):
        try:
            return (b for b in self.binders if b.accept(aType)).next()
        except StopIteration:
            return None

    def provide(self, aType):
        binder = self.accept(aType)
        if binder:
            return binder.provider().get(self)
        else:
            return None
