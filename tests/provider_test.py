# Copyright (C)2016 D. Plaindoux.
#
# This program is free software; you can redistribute it and/or modify it
# under the terms of the GNU Lesser General Public License as published by
# the Free Software Foundation; either version 2, or (at your option) any
# later version.

import unittest
from fluent_rest.exceptions import OverloadedProviderException
from fluent_rest.spec.rest import *


class TestCase(unittest.TestCase):
    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_should_have_a_provider(self):
        @Provider(TestCase)
        def test():
            pass

        self.assertTrue(specification(test).hasGivenProvider(TestCase))

    def test_should_not_have_a_two_providers(self):
        try:
            @Provider(TestCase)
            @Provider(Provider)
            def test():
                pass

            self.fail('Cannot have more than one provider')
        except OverloadedProviderException, _:
            pass


def suite():
    aSuite = unittest.TestSuite()
    aSuite.addTest(unittest.makeSuite(TestCase))
    return aSuite


if __name__ == '__main__':
    unittest.main()
