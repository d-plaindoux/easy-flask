"""
Werkzeug bridge
"""
from fluent_rest.engine.request import Request
from fluent_rest.inspector.inspection import inspect

from werkzeug import wrappers


class WerkzeugBridge:
    def __init__(self):
        self.__services = []
        pass

    def __request(self, request):
        return Request

    @wrappers.Request.application
    def __trigger(self, request):
        return wrappers.Response('Hello %s!' % request.data)

    def addService(self, service):
        inspected = inspect(service)

    def removeService(self, service):
        pass

    def bind(self, binder):
        binder(self.__trigger)


if __name__ == '__main__':
    from werkzeug.serving import run_simple

    WerkzeugBridge().bind(lambda a: run_simple('localhost', 4000, a))
