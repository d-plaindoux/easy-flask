"""
Werkzeug bridge
"""
from fluent_rest.engine.filter import SpecificationFilter
from fluent_rest.engine.request import Request
from fluent_rest.inspector.inspection import inspect
from fluent_rest.spec.rest import GET, Path, Consumes, Produces


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

    def __trigger(self, request):
        wrapper = self.request_wrapper(request)
        for s in self.__filters:
            instance = s.filter(wrapper)
            if instance:
                response = instance.execute(request.get_data())
                return self.response_wrapper(response)

        return self.failure_wrapper(404)

    def install(self, service):
        self.__filters.extend(inspect(service).handle(SpecificationFilter))

    def uninstall(self, service):
        pass

    def bind(self, binder):
        binder(self.__trigger)


class Werkzeug(WSGIBridge):
    def __init__(self):
        WSGIBridge.__init__(self)

    def request_wrapper(self, request):
        return Request(request.method,
                       request.path,
                       request.headers['CONTENT-TYPE'],
                       request.headers['CONTENT-TYPE'])  # TODO(didier) ???

    def response_wrapper(self, response):
        from werkzeug import wrappers

        return wrappers.Response(response)

    def failure_wrapper(self, status, message=None):
        from werkzeug import wrappers

        return wrappers.BaseResponse(status=status, response=message)


if __name__ == '__main__':
    from werkzeug import serving
    from werkzeug import wrappers

    bridge = Werkzeug()

    @GET
    @Path("/{name}")
    @Consumes("application/json")
    @Produces("application/json")
    def test(surname, name):
        return "Hello from %s %s!" % (name, surname)

    bridge.install(test)

    bridge.bind(
        lambda a: serving.run_simple('localhost',
                                     4000,
                                     wrappers.Request.application(a))
    )

