fluent-rest
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


class TodoNotFound(Exception):
    pass


@Path("/todo")
@Consumes("application/json")
@Produces("application/json")
class Todo:
    def __init__(self):
        self.Todo = {}

    @GET
    def list(self):
        return self.Todo

    @GET
    @Path("{id:uuid}")
    def get(self, id):
        if id in self.Todo:
            return self.Todo[id]
        else:
            raise TodoNotFound()

    @POST
    def create(self, data):
        id = uuid.uuid1()
        self.Todo[id] = data
        return id

    @PUT
    @Path("{id:uuid}")
    def modify(self, id, data):
        if id in self.Todo:
            self.Todo[id] = data
            return id
        else:
            raise TodoNotFound()

    @DELETE
    @Path("{id:uuid}")
    def remove(self, id):
        # deletes an identified Todo
        if id in self.Todo:
            del self.Todo[id]
            return id
        else:
            raise TodoNotFound()

    @Provider(TodoNotFound)
    def Todo(self, bridge, _):
        return bridge.failure(404)
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

`@Consumes(...)` and `@Produces(...)`
-------------------------------------------------------------------------------

Each request comes with its constraints related to input and output
representation. This is commonly denoted using mime and each of it has it
own transformation process.

`@GET`, `@POST`, `@PUT`, `@DELETE` ...
-------------------------------------------------------------------------------

`@Provider(...)`
-------------------------------------------------------------------------------


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
