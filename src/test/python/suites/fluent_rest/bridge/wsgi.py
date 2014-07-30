"""
TODO
"""

import unittest
from uuid import uuid1
from fluent_rest.bridge.wsgi import WSGIBridge
from fluent_rest.engine.request import Request
from fluent_rest.spec.rest import *


class TestWSGIBridge(WSGIBridge):
    def __init__(self):
        WSGIBridge.__init__(self)

    def request_wrapper(self, request):
        return request

    def response_wrapper(self, response):
        return response

    def failure_wrapper(self, status, message=None):
        return status


@Path("/todo")
@Consumes("application/json")
@Produces("application/json")
class TODO:
    def __init__(self):
        self.todo = {}

    @GET
    def list(self):
        # returns todo
        return self.todo

    @GET
    @Path("{id:uuid}")
    def get(self, id):
        if id in self.todo:
            return self.todo[id]
        else:
            raise Exception("Not found")

    @POST
    def create(self, data):
        # creates a now todo using `data`
        id = uuid1()
        self.todo[id] = data
        return None

    @PUT
    @Path("{id:uuid}")
    def modify(self, id, data):
        # modifies an identified todo using `data`
        if id in self.todo:
            self.todo[id] = data
            return None
        else:
            raise Exception("Not found")

    @DELETE
    @Path("{id:uuid}")
    def remove(self, id):
        # deletes an identified todo
        if id in self.todo:
            del self.todo[id]
            return None
        else:
            raise Exception("Not found")


class TestCase(unittest.TestCase):
    def setUp(self):
        self.server = TestWSGIBridge()
        self.server.install(TODO())

    def tearDown(self):
        pass

    def test_should_have_empty_todo(self):
        request = Request.get("/todo",
                              "application/json",
                              "application/json")

        response = self.server.trigger(request)

        self.assertEqual({}, response)

    def test_should_have_post_todo(self):
        request = Request.post("/todo",
                               "application/json",
                               "application/json",
                               '{"a":12}')

        response = self.server.trigger(request)

        self.assertEqual(None, response)

    def test_should_have_one_todo_after_post_todo(self):
        request = Request.post("/todo",
                               "application/json",
                               "application/json",
                               '{"a":12}')

        self.server.trigger(request)

        request = Request.post("/todo",
                               "application/json",
                               "application/json",
                               '{"a":12}')

        response = self.server.trigger(request)

        self.assertNotEqual({}, response)


def suite():
    aSuite = unittest.TestSuite()
    aSuite.addTest(unittest.makeSuite(TestCase))
    return aSuite


if __name__ == '__main__':
    unittest.main()
