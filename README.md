fluent-rest [![Build Status](https://travis-ci.org/d-plaindoux/fluent-rest.svg?branch=master)](https://travis-ci.org/d-plaindoux/fluent-rest)
===============================================================================

Fluent REST decorators (annotations) dedicated to Web framework like:
* [Flask](http://flask.pocoo.org)
* [Django](http://www.django-rest-framework.org)
* [Pecan](http://www.pecanpy.org) and
* [Falcon](http://falconframework.org).

Introduction
===============================================================================

This library provides REST specification facilities dedicated to
python web frameworks.

`Todo` Example
===============================================================================

In this example we show how decorators can be used in order to specify a REST
service dedicated to `Todo` data.

```python
from fluent_rest.rest import *
from fluent_rest.response import WebException


class TodoNotFound(Exception):
    def __init__(id):
        self.id = id


@Path("/todo")
@Consumes("application/json")
@Produces("application/json")
class Todo:
    def __init__(self):
        self.__todo = {}

    @GET
    def list(self):
        return self.__todo

    @GET
    @Path("{id:uuid}")
    def get(self, id):
        if id in self.__todo:
            return self.__todo[id]
        else:
            raise TodoNotFound(id)

    @POST
    def create(self, data):
        id = uuid.uuid1()
        self.__todo[id] = data
        return id

    @PUT
    @Path("{id:uuid}")
    def modify(self, id, data):
        if id in self.__todo:
            self.__todo[id] = data
            return id
        else:
            raise TodoNotFound(id)

    @DELETE
    @Path("{id:uuid}")
    def remove(self, id):
        if id in self.__todo:
            del self.__todo[id]
            return id
        else:
            raise TodoNotFound(id)

    @Provider(TodoNotFound)
    def notFound(e):
        raise WebException.notFound("todo %s not found" % e.id)
```

Then creating a WSGI server instance based on utility library like
[Werkzeug](http://werkzeug.pocoo.org) can be easily done using provided
bridge.

```python
from werkzeug import serving
from werkzeug import wrappers
from fluent_rest.bridge import Werkzeug

bridge = Werkzeug()

bridge.register(Todo())

bridge.bind(
    lambda a: serving.run_simple('localhost',
                                 4000,
                                 wrappers.Request.application(a))
)
```

Decorators
===============================================================================

The fluent-rest library provides a set of decorators applied at the
class or at the method level. Decorators at the class level define
specification which are general like the path and available encoders and
decoders. At the method level verbs are required and additional path can
also be specified completing the class level path.

`@Path(path)`
-------------------------------------------------------------------------------

A path decorator defines the path associated to a given REST service. A path
corresponds to an URI to which a resource respond. Such path can be a simple
 URI or a template URI. A template URI defines typed variables bound
at the runtime.

### Syntax

```
path = '/'? item ('/' item)* '/'?

item = '{' IDENT (':' type) '}'
     | (CHAR - {'/','{'})+

type = 'int' | 'float' | 'string' | 'path' | 'uuid'
```

### Examples

The path specficiation `/foo/{bar:string}/baz` matches path like
`/foo/a-string/baz` binding  `bar` variable to `a-string` ; match does not
succeed for path like  `/foo/a/string/baz` because `a/string` is a sub path.
 For this purpose the path type has been proposed and can be used to bind a
 sub path. Then the path specification `/foo/{bar:path}/baz` matches
 `/foo/a/string/baz` binding `bar` to `a/string` sub path.

### Extending path types

TODO

`@Consumes(mime)` and `@Produces(mime)`
-------------------------------------------------------------------------------

Each request comes with its constraints related to input and output
representation. This is commonly denoted using mime and each of it has it
own transformation process.

`@GET`, `@POST`, `@PUT`, `@DELETE` and `@Verb(verb)`
-------------------------------------------------------------------------------

In the REST approach the method - or verb - is fundamental.  The primary HTTP
verbs are POST, GET, PUT, and DELETE. These correspond respectively to
create, read, update, and delete operations aka CRUD model.. There are a
number of other verbs, too, but are utilized less frequently. For this
category of verbs the specification is done using `@Verb(...)` decorator.

`@Provider(Class)`
-------------------------------------------------------------------------------

A provider in different situations like:
- exception mapping transforming an exception to a `WebException`
- create a resource on demand

`@Inject(Class)`
-------------------------------------------------------------------------------

TODO

License
===============================================================================

Copyright (C)2014 D. Plaindoux.

This program is free software; you can redistribute it and/or modify
it under the terms of the GNU Lesser General Public License as published
by the Free Software Foundation; either version 2, or (at your option)
any later version.

This program is distributed in the hope that it will be useful, but
WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY
or FITNESS FOR A PARTICULAR PURPOSE. See the GNU Lesser General Public License
for more details.

You should have received a copy of the GNU Lesser General Public License
along with this program; see the file COPYING. If not, write to the Free
Software Foundation, 675 Mass Ave, Cambridge, MA 02139, USA.
