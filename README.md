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

Work in progress
================

```python
from fluent_rest.rest import *

class TODO:
    def __init__(self):
        pass

    @GET @Path("todo")
    @Produces("application/json")
    def listTodo(self):
        # returns todo
        ...

    @GET @Path("todo/<id>")
    @Produces("application/json")
    def get(self, id):
        # returns identified todo
        ...

    @POST @Path("todo")
    @Consumes("application/json")
    @Produces("application/json")
    def create(self, data):
        # creates a now todo using `data`
        ...

    @PUT @Path("todo/<id>")
    @Consumes("application/json")
    @Produces("application/json")
    def modify(self, id, data):
        # modifies an identified todo using `data`
        ...

    @DELETE @Path("todo/<id>")
    @Consumes("application/json")
    def remove(self, id):
        # deletes an identified todo
        ...
```

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
