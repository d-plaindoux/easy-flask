easy-flask
==========

Fluent REST decorators (annotations) dedicated to Flask framework

Introduction
============

This library provides REST specification facilities dedicated to
python frameworks like (Flask)[http://flask.pocoo.org] first.

Work in progress
================

```python
@rest.Path(...)
@rest.GET
@rest.PUT
@rest.POST
@rest.DELETE
@rest.Verb(...)
@rest.Consumes(@rest.type.APPLICATION_JSON)
@rest.Produces(@rest.type.APPLICATION_JSON)
@rest.Asynchronous
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