fluent-rest
===========

Fluent REST decorators (annotations) dedicated to Web framework like:
* [Flask](http://flask.pocoo.org)
* [Django](http://www.django-rest-framework.org)
* [Pecan](http://www.pecanpy.org) and
* [Falcon](http://falconframework.org).

Introduction
============

This library provides REST specification facilities dedicated to
python web frameworks.

`TODO` Example
==============

In this example we show how decorators can be used in order to specify a REST
service dedicated to `TODO` data.

```python
from fluent_rest.rest import *

@Path("todo")
@Consumes("application/json")
@Produces("application/json")
class TODO:
    def __init__(self):
        pass

    @GET
    def list(self):
        # returns todo
        ...

    @GET @Path("{id:uuid}")
    def get(self, id):
        # returns identified todo
        ...

    @POST
    def create(self, data):
        # creates a now todo using `data`
        ...

    @PUT @Path("{id:uuid}")
    def modify(self, id, data):
        # modifies an identified todo using `data`
        ...

    @DELETE @Path("{id:uuid}")
    def remove(self, id):
        # deletes an identified todo
        ...
```

Decorators
==========

The fluent-rest library provides a set of decorators applied at the
class or at the method level. Decorators at the class level define
specification which are general like the path and available encoders and
decoders. At the method level verbs are required and additional path can
also be specified completing the class level path.

Path decorator `@Path(path)`
----------------------------

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

Codec decorators
----------------

Verb decorators
---------------

License
=======

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
