import unittest

from fluent_rest.spec.path import *


class TestCase(unittest.TestCase):
    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_should_parse_single_item_foo(self):
        self.assertEquals(Path.parse('foo'),
                          Path(['foo']))

    def test_should_parse_single_item_bar(self):
        self.assertEquals(Path.parse('bar'),
                          Path(['bar']))

    def test_should_parse_item_foo_bar(self):
        self.assertEquals(Path.parse('foo/bar'),
                          Path(['foo', 'bar']))

    def test_should_parse_item_bar_foo(self):
        self.assertEquals(Path.parse('bar/foo'),
                          Path(['bar', 'foo']))

    def test_should_parse_item_baz_bar_foo(self):
        self.assertEquals(Path.parse('baz/bar/foo'),
                          Path(['baz', 'bar', 'foo']))

    def test_should_parse_a_variable_myid(self):
        self.assertEquals(Path.parse('{myid}'),
                          Path([Var('myid')]))

    def test_should_parse_a_variable_anotherid(self):
        self.assertEquals(Path.parse('{anotherid}'),
                          Path([Var('anotherid')]))

    def test_should_parse_a_variable_myid_as_a_path(self):
        self.assertEquals(Path.parse('{myid:path}'),
                          Path([Var('myid', 'path')]))

    def test_should_parse_a_complex_path(self):
        self.assertEquals(Path.parse('file/{myid:string}/content'),
                          Path(['file', Var('myid', 'string'), 'content']))


def suite():
    aSuite = unittest.TestSuite()
    aSuite.addTest(unittest.makeSuite(TestCase))
    return aSuite


if __name__ == '__main__':
    unittest.main()
