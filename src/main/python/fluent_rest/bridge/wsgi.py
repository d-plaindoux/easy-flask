"""
Werkzeug bridge
"""
from fluent_rest.engine.filter import SpecificationFilter
from fluent_rest.engine.request import Request
from fluent_rest.inspector.inspection import inspect


class WSGIBridge:
    def __init__(self):
        self.__filters = []
        pass

    def request_wrapper(self, request):
        raise NotImplemented()

    def response_wrapper(self, response):
        raise NotImplemented()

    def failure_wrapper(self, status, message=None):
        raise NotImplemented()

    def trigger(self, request):
        wrapper = self.request_wrapper(request)
        for s in self.__filters:
            instance = s.filter(wrapper)
            if instance:
                response = instance.execute(wrapper.data())
                return self.response_wrapper(response)

        return self.failure_wrapper(404)

    def install(self, service):
        self.__filters.extend(inspect(service).handle(SpecificationFilter))

    def uninstall(self, service):
        pass

    def bind(self, binder):
        binder(self.trigger)


class Werkzeug(WSGIBridge):
    def __init__(self):
        WSGIBridge.__init__(self)

    def request_wrapper(self, request):
        return Request(request.method,
                       request.path,
                       request.headers['CONTENT-TYPE'],
                       request.headers['CONTENT-TYPE'],     # TODO(didier) ???
                       request.get_data())                  # TODO(didier) ???

    def response_wrapper(self, response):
        from werkzeug import wrappers

        return wrappers.Response(response)

    def failure_wrapper(self, status, message=None):
        from werkzeug import wrappers

        return wrappers.BaseResponse(status=status, response=message)
