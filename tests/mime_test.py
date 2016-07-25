# Copyright (C)2016 D. Plaindoux.
#
# This program is free software; you can redistribute it and/or modify it
# under the terms of the GNU Lesser General Public License as published by
# the Free Software Foundation; either version 2, or (at your option) any
# later version.

import unittest
from fluent_rest.spec.rest import *


class TestCase(unittest.TestCase):
    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_should_have_a_consumes(self):
        @Consumes('application/json')
        def test():
            pass

        self.assertTrue(
            specification(test).hasGivenConsumes('application/json'))

    def test_should_have_two_consumes(self):
        @Consumes('application/json')
        @Consumes('application/xml')
        def test():
            pass

        self.assertTrue(
            specification(test).hasGivenConsumes('application/json'))
        self.assertTrue(
            specification(test).hasGivenConsumes('application/xml'))

    def test_should_have_a_produces(self):
        @Produces('application/json')
        def test():
            pass

        self.assertTrue(
            specification(test).hasGivenProduces('application/json'))

    def test_should_have_two_produces(self):
        @Produces('application/json')
        @Produces('application/xml')
        def test():
            pass

        self.assertTrue(
            specification(test).hasGivenProduces('application/json'))
        self.assertTrue(
            specification(test).hasGivenProduces('application/xml'))

    def test_should_identity_producer(self):
        @Produces('application/json', lambda e: e)
        def test():
            pass

        self.assertTrue(
            specification(test).hasGivenProduces('application/json'))
        self.assertTrue(
            specification(test).getGivenProduces('application/json')(True))

    def test_should_not_identity_producer(self):
        @Produces('application/json', lambda e: not e)
        def test():
            pass

        self.assertTrue(
            specification(test).hasGivenProduces('application/json'))
        self.assertTrue(
            specification(test).getGivenProduces('application/json')(False))


def suite():
    aSuite = unittest.TestSuite()
    aSuite.addTest(unittest.makeSuite(TestCase))
    return aSuite


if __name__ == '__main__':
    unittest.main()
