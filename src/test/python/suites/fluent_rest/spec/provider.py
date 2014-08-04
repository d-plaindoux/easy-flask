# Copyright (C)2014 D. Plaindoux.
#
# This program is free software; you can redistribute it and/or modify it
# under the terms of the GNU Lesser General Public License as published by
# the Free Software Foundation; either version 2, or (at your option) any
# later version.

import unittest
from fluent_rest.spec.rest import *
from fluent_rest.exceptions import OverloadedVerbException, OverloadedProviderException


class TestCase(unittest.TestCase):
    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_should_have_Provider(self):
        @Provider(Exception)
        def test():
            pass

        self.assertTrue(specs(test).hasProvider())

    def test_should_not_have_more_than_one_Providers(self):
        try:
            @Provider(Exception)
            @Provider(Exception)
            def test_with_two_providers():
                pass

                self.fail('Cannot have more than one provider')

        except OverloadedProviderException, _:
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
