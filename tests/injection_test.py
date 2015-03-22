# Copyright (C)2015 D. Plaindoux.
#
# This program is free software; you can redistribute it and/or modify it
# under the terms of the GNU Lesser General Public License as published by
# the Free Software Foundation; either version 2, or (at your option) any
# later version.

import unittest
from fluent_rest.spec.injection import Binder
from fluent_rest.spec.injection import ClassMethodProvider
from fluent_rest.spec.injection import ClassProvider
from fluent_rest.spec.injection import FunctionProvider
from fluent_rest.spec.injection import Injection
from fluent_rest.spec.injection import InstanceMethodProvider
from fluent_rest.spec.injection import InstanceProvider


class TestCase(unittest.TestCase):
    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_should_accept_a_type(self):
        self.assertTrue(
            Binder(TestCase, lambda _: _).accept(TestCase)
        )

    def test_should_not_accept_a_type(self):
        self.assertFalse(
            Binder(TestCase, lambda _: _).accept(Binder)
        )

    def test_should_not_accept_a_sub_type(self):
        self.assertFalse(
            Binder(TestCase, lambda _: _).accept(unittest.TestCase)
        )

    def test_should_add_a_provider(self):
        injection = Injection()
        self.assertTrue(
            injection.bind(TestCase, lambda _: _).accept(TestCase)
        )

    def test_should_add_a_function_provider(self):
        injection = Injection()
        self.assertIsInstance(
            injection.bind(TestCase, lambda _: _).accept(TestCase).provider(),
            FunctionProvider
        )

    def test_should_add_a_class_provider(self):
        class T:
            pass

        injection = Injection()
        self.assertIsInstance(
            injection.bind(TestCase, T).accept(TestCase).provider(),
            ClassProvider
        )

    def test_should_add_an_instance_provider(self):
        class T(TestCase):
            def __init__(self):
                pass

        injection = Injection()
        self.assertIsInstance(
            injection.bind(TestCase, T()).accept(TestCase).provider(),
            InstanceProvider
        )

    def test_should_add_a_class_method_provider(self):
        class T:
            def m(self):
                pass

        injection = Injection()
        self.assertIsInstance(
            injection.bind(TestCase, T.m).accept(TestCase).provider(),
            ClassMethodProvider
        )

    def test_should_add_an_instance_method_provider(self):
        class T:
            def m(self):
                pass

        injection = Injection()
        self.assertIsInstance(
            injection.bind(TestCase, T().m).accept(TestCase).provider(),
            InstanceMethodProvider
        )


def suite():
    aSuite = unittest.TestSuite()
    aSuite.addTest(unittest.makeSuite(TestCase))
    return aSuite


if __name__ == '__main__':
    unittest.main()
