# Copyright (C)2014 D. Plaindoux.
#
# This program is free software; you can redistribute it and/or modify it
# under the terms of the GNU Lesser General Public License as published by
# the Free Software Foundation; either version 2, or (at your option) any
# later version.

import unittest
from fluent_rest.spec.rest import *
from fluent_rest.exceptions import OverloadedVerbException


class TestCase(unittest.TestCase):
    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_should_have_GET(self):
        @GET
        def test():
            pass

        self.assertTrue(specs(test).hasGivenVerb(u'GET'))

    def test_should_have_PUT(self):
        @PUT
        def test():
            pass

        self.assertTrue(specs(test).hasGivenVerb(u'PUT'))

    def test_should_have_POST(self):
        @POST
        def test():
            pass

        self.assertTrue(specs(test).hasGivenVerb(u'POST'))

    def test_should_have_DELETE(self):
        @DELETE
        def test():
            pass

        self.assertTrue(specs(test).hasGivenVerb(u'DELETE'))

    def test_should_have_a_Verb(self):
        @Verb(u'UPLOAD')
        def test():
            pass

        self.assertTrue(specs(test).hasGivenVerb(u'UPLOAD'))

    def test_should_not_have_GET_and_PUT(self):
        try:
            @GET
            @PUT
            def test_function_to_be_rejected():
                pass

            self.fail('Cannot have more than one verb')
        except OverloadedVerbException, _:
            pass

    def test_should_have_GET_in_class(self):
        @GET
        class Test:
            def __init__(self):
                pass

        self.assertTrue(specs(Test).hasGivenVerb(u'GET'))


def suite():
    aSuite = unittest.TestSuite()
    aSuite.addTest(unittest.makeSuite(TestCase))
    return aSuite


if __name__ == '__main__':
    unittest.main()
