# Copyright (C)2014 D. Plaindoux.
#
# This program is free software; you can redistribute it and/or modify it
# under the terms of the GNU Lesser General Public License as published by
# the Free Software Foundation; either version 2, or (at your option) any
# later version.

import unittest

from uuid import uuid1
from fluent_rest.spec.path import *


class TestCase(unittest.TestCase):
    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_should_match_a_simple_path(self):
        self.assertIsNotNone(Path.parse('bar/foo').accept('bar/foo'))

    def test_should_match_a_path_with_a_variable(self):
        variables = Path.parse('bar/{foo}').accept('bar/tutu')
        self.assertIsNotNone(variables)
        self.assertEquals(variables('foo'), 'tutu')

    def test_should_match_a_path_with_a_string_variable(self):
        variables = Path.parse('bar/{foo:string}').accept('bar/tutu')
        self.assertIsNotNone(variables)
        self.assertEquals(variables('foo'), 'tutu')

    def test_should_match_a_path_with_an_int_variable(self):
        variables = Path.parse('bar/{foo:int}').accept('bar/123')
        self.assertIsNotNone(variables)
        self.assertEquals(variables('foo'), 123)

    def test_should_match_a_path_with_a_negative_int_variable(self):
        variables = Path.parse('bar/{foo:int}').accept('bar/-123')
        self.assertIsNotNone(variables)
        self.assertEquals(variables('foo'), -123)

    def test_should_match_a_path_with_an_float_variable(self):
        variables = Path.parse('bar/{foo:float}').accept('bar/123')
        self.assertIsNotNone(variables)
        self.assertEquals(variables('foo'), 123.0)

    def test_should_match_a_path_with_an_complex_float_variable(self):
        variables = Path.parse('bar/{foo:float}').accept('bar/123e12')
        self.assertIsNotNone(variables)
        self.assertEquals(variables('foo'), 123.0E12)

    def test_should_not_match_a_path_with_an_int_variable(self):
        variables = Path.parse('bar/{foo:int}').accept('bar/aaa')
        self.assertIsNone(variables)

    def test_should_not_match_a_path_with_a_path_variable(self):
        variables = Path.parse('bar/{foo:path}/c').accept('bar/a/b/c')

        self.assertIsNotNone(variables)
        self.assertEquals(variables('foo'), 'a/b')

    def test_should_not_match_a_path_with_a_uuid_variable(self):
        uuid = uuid1()
        variables = Path.parse('bar/{foo:uuid}/c').accept('bar/%s/c' % uuid)

        self.assertIsNotNone(variables)
        self.assertEquals(variables('foo'), uuid)

    def test_should_not_match_a_path_with_special_characters(self):
        variables = Path.parse('bar/$[a-A]').accept('bar/$[a-A]')

        self.assertIsNotNone(variables)


def suite():
    aSuite = unittest.TestSuite()
    aSuite.addTest(unittest.makeSuite(TestCase))
    return aSuite


if __name__ == '__main__':
    unittest.main()
