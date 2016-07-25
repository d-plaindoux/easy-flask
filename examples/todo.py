# Copyright (C)2016 D. Plaindoux.
#
# This program is free software; you can redistribute it and/or modify it
# under the terms of the GNU Lesser General Public License as published by
# the Free Software Foundation; either version 2, or (at your option) any
# later version.

from json import dumps
from uuid import uuid1

from fluent_rest.bridge.werkzeugbridge import WerkzeugBridge
from fluent_rest.runtime.response import WebException
from fluent_rest.spec import *
from werkzeug import serving
from werkzeug import wrappers


#
# Transformation processes
#


class TodoNotFound(Exception):
    def __init__(self, identifier):
        self.identifier = identifier


def UUIDToString(uuid):
    return str(uuid)


def TodoToJson(dictionary):
    result = {}
    for key in dictionary.keys():
        result[str(key)] = dictionary[key]
    return dumps(result)


@Provider(TodoNotFound)
def notFound(e):
    raise WebException.notFound("todo %s not found" % e.identifier)


@Path("/todo")
@Consumes("application/json")
class Todo:
    def __init__(self):
        self.__todo = {}

    @GET
    @Produces("application/json", TodoToJson)
    def list(self):
        return self.__todo

    @GET
    @Path("{id:uuid}")
    @Produces("application/json")
    def get(self, id):
        if id in self.__todo:
            return self.__todo[id]
        else:
            raise TodoNotFound(id)

    @POST
    @Produces("application/json", UUIDToString)
    def create(self, data):
        id = uuid1()
        self.__todo[id] = data
        return id

    @PUT
    @Path("{id:uuid}")
    @Produces("application/json", UUIDToString)
    def modify(self, id, data):
        if id in self.__todo:
            self.__todo[id] = data
            return id
        else:
            raise TodoNotFound(id)

    @DELETE
    @Path("{id:uuid}")
    @Produces("application/json", UUIDToString)
    def remove(self, id):
        if id in self.__todo:
            del self.__todo[id]
            return id
        else:
            raise TodoNotFound(id)


if __name__ == '__main__':
    bridge = WerkzeugBridge(). \
        register(notFound). \
        register(Todo). \
        bind(lambda a: serving.run_simple('localhost',
                                          4000,
                                          wrappers.Request.application(a)))
