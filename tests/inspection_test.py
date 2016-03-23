# Copyright (C)2015 D. Plaindoux.
#
# This program is free software; you can redistribute it and/or modify it
# under the terms of the GNU Lesser General Public License as published by
# the Free Software Foundation; either version 2, or (at your option) any
# later version.

import unittest
from fluent_rest.spec.rest import *
from fluent_rest.spec.inspection import inspector


class TestCase(unittest.TestCase):
    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_should_inspect_function(self):
        @GET
        @Path('bar')
        @Consumes('application/json')
        def test():
            pass

        self.assertEquals(inspector(test).handle(lambda f: f), [test])

    def test_should_inspect_class(self):
        class Test:
            def __init__(self):
                pass

            @GET
            @Path('bar')
            @Consumes('application/json')
            def test(self):
                pass

        self.assertEquals(inspector(Test).handle(lambda f: f), [Test.test])

    def test_should_inspect_instance(self):
        class Test:
            def __init__(self):
                pass

            @GET
            @Path('bar')
            @Consumes('application/json')
            def test(self):
                pass

        test = Test()

        self.assertEquals(inspector(test).handle(lambda f: f), [test.test])

    def test_should_inspect_specified_class_extending_path(self):
        @Path('foo')
        class Test:
            def __init__(self):
                pass

            @GET
            @Path('bar')
            @Consumes('application/json')
            def test(self):
                pass

        self.assertEquals(inspector(Test).handle(lambda f: f), [Test.test])
        self.assertEquals(specification(Test.test).getPath(), 'foo/bar')

    def test_should_inspect_specified_instance_extending_path(self):
        @Path('foo')
        class Test:
            def __init__(self):
                pass

            @GET
            @Path('bar')
            @Consumes('application/json')
            def test(self):
                pass

        test = Test()

        self.assertEquals(inspector(test).handle(lambda f: f), [test.test])
        self.assertEquals(specification(test.test).getPath(), 'foo/bar')

    def test_should_inspect_specified_class_adding_path(self):
        @Path('foo')
        class Test:
            def __init__(self):
                pass

            @GET
            @Consumes('application/json')
            def test(self):
                pass

        self.assertEquals(inspector(Test).handle(lambda f: f), [Test.test])
        self.assertEquals(specification(Test.test).getPath(), 'foo')

    def test_should_inspect_specified_class_adding_consumes(self):
        @Path('foo')
        @Consumes('application/json')
        class Test:
            def __init__(self):
                pass

            @GET
            @Path('bar')
            def test(self):
                pass

        self.assertEquals(inspector(Test).handle(lambda f: f), [Test.test])
        self.assertTrue(
            specification(Test.test).hasGivenConsumes('application/json'))

    def test_should_inspect_specified_adding_produces(self):
        @Path('foo')
        @Produces('application/json')
        class Test:
            def __init__(self):
                pass

            @GET
            def test(self):
                pass

        self.assertEquals(inspector(Test).handle(lambda f: f), [Test.test])
        self.assertTrue(
            specification(Test.test).hasGivenProduces('application/json'))


def suite():
    aSuite = unittest.TestSuite()
    aSuite.addTest(unittest.makeSuite(TestCase))
    return aSuite


if __name__ == '__main__':
    unittest.main()
