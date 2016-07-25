# Copyright (C)2016 D. Plaindoux.
#
# This program is free software; you can redistribute it and/or modify it
# under the terms of the GNU Lesser General Public License as published by
# the Free Software Foundation; either version 2, or (at your option) any
# later version.

import unittest
import uuid

from fluent_rest.bridge.wsgibridge import WSGIBridge
from fluent_rest.runtime.request import Request
from fluent_rest.runtime.response import WebException
from fluent_rest.spec.rest import Consumes
from fluent_rest.spec.rest import DELETE
from fluent_rest.spec.rest import GET
from fluent_rest.spec.rest import POST
from fluent_rest.spec.rest import PUT
from fluent_rest.spec.rest import Path
from fluent_rest.spec.rest import Produces
from fluent_rest.spec.rest import Provider


class TestWSGIBridge(WSGIBridge):
    def __init__(self):
        WSGIBridge.__init__(self)

    def request(self, request):
        return request

    def response(self, response):
        return response

    def failure(self, status, message=None):
        return status


class TodoNotFound(Exception):
    def __init__(self, id):
        self.id = id


class Result:
    def __init__(self, result):
        self.result = result


@Path("/todo")
@Consumes("application/json")
@Produces("application/json")
class Todo:
    def __init__(self):
        self.todo = {}

    @GET
    def list(self):
        return Result(self.todo)

    @GET
    @Path("{id:uuid}")
    def get(self, id):
        if id in self.todo:
            return Result(self.todo[id])
        else:
            raise TodoNotFound(id)

    @POST
    def create(self, data):
        id = uuid.uuid1()
        self.todo[id] = data
        return Result(id)

    @PUT
    @Path("{id:uuid}")
    def modify(self, id, data):
        if id in self.todo:
            self.todo[id] = data
            return Result(id)
        else:
            raise TodoNotFound(id)

    @DELETE
    @Path("{id:uuid}")
    def remove(self, id):
        if id in self.todo:
            del self.todo[id]
            return Result(id)
        else:
            raise TodoNotFound(id)

    @Provider(Result)
    def returns(self, r):
        return r.result

    @Provider(TodoNotFound)
    def notFound(self, e):
        raise WebException.notFound("todo %s not found" % e.id)


class TestCaseWithInstance(unittest.TestCase):
    def setUp(self):
        self.bridge = TestWSGIBridge().register(Todo())

    def tearDown(self):
        pass

    def test_should_have_empty_todo(self):
        request = Request.get("/todo",
                              "application/json",
                              "application/json")

        response = self.bridge.trigger(request)

        self.assertEqual({}, response)

    def test_should_have_no_todo(self):
        request = Request.get("/todo/%s" % uuid.uuid1(),
                              "application/json",
                              "application/json")

        response = self.bridge.trigger(request)

        self.assertEqual(404, response)

    def test_should_have_post_todo(self):
        request = Request.post("/todo",
                               "application/json",
                               "application/json",
                               '{"a":12}')

        response = self.bridge.trigger(request)

        self.assertIsNotNone(response)

    def test_should_have_one_todo_after_post_todo(self):
        request = Request.post("/todo",
                               "application/json",
                               "application/json",
                               '{"a":12}')

        id = self.bridge.trigger(request)

        request = Request.get("/todo",
                              "application/json",
                              "application/json")

        response = self.bridge.trigger(request)

        self.assertNotEqual({}, response)
        self.assertIsNotNone(response[id])

    def test_should_not_delete_todo(self):
        request = Request.delete("/todo/%s" % uuid.uuid1(),
                                 "application/json",
                                 "application/json")

        response = self.bridge.trigger(request)

        self.assertEqual(404, response)

    def test_should_delete_created_todo(self):
        request = Request.post("/todo",
                               "application/json",
                               "application/json",
                               '{"a":12}')

        id = self.bridge.trigger(request)

        request = Request.delete("/todo/%s" % id,
                                 "application/json",
                                 "application/json")

        response = self.bridge.trigger(request)

        self.assertEqual(id, response)


class TestCaseWithClass(unittest.TestCase):
    def setUp(self):
        self.bridge = TestWSGIBridge().register(Todo)

    def tearDown(self):
        pass

    def test_should_have_empty_todo(self):
        request = Request.get("/todo",
                              "application/json",
                              "application/json")

        response = self.bridge.trigger(request)

        self.assertEqual({}, response)

    def test_should_have_no_todo(self):
        request = Request.get("/todo/%s" % uuid.uuid1(),
                              "application/json",
                              "application/json")

        response = self.bridge.trigger(request)

        self.assertEqual(404, response)

    def test_should_have_post_todo(self):
        request = Request.post("/todo",
                               "application/json",
                               "application/json",
                               '{"a":12}')

        response = self.bridge.trigger(request)

        self.assertIsNotNone(response)

    def test_should_not_have_one_todo_after_post_todo(self):
        request = Request.post("/todo",
                               "application/json",
                               "application/json",
                               '{"a":12}')

        id = self.bridge.trigger(request)

        request = Request.get("/todo",
                              "application/json",
                              "application/json")

        response = self.bridge.trigger(request)

        self.assertEqual({}, response)

    def test_should_not_delete_todo(self):
        request = Request.delete("/todo/%s" % uuid.uuid1(),
                                 "application/json",
                                 "application/json")

        response = self.bridge.trigger(request)

        self.assertEqual(404, response)

    def test_should_not_delete_created_todo(self):
        request = Request.post("/todo",
                               "application/json",
                               "application/json",
                               '{"a":12}')

        response = self.bridge.trigger(request)

        request = Request.delete("/todo/%s" % response,
                                 "application/json",
                                 "application/json")

        response = self.bridge.trigger(request)

        self.assertEqual(404, response)


def suite():
    aSuite = unittest.TestSuite()
    aSuite.addTest(unittest.makeSuite(TestCaseWithInstance))
    aSuite.addTest(unittest.makeSuite(TestCaseWithClass))
    return aSuite


if __name__ == '__main__':
    unittest.main()
