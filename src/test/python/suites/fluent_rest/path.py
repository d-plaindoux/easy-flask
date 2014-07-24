import unittest
from fluent_rest.path import *


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

    def test_should_match_a_simple_path(self):
        self.assertIsNotNone(Path.parse('bar/foo').accept('bar/foo'))

    def test_should_match_a_path_with_a_variable(self):
        variables = Path.parse('bar/{foo}').accept('bar/tutu')
        self.assertIsNotNone(variables)
        self.assertEquals(variables['foo'], 'tutu')

    def test_should_match_a_path_with_an_int_variable(self):
        variables = Path.parse('bar/{foo:int}').accept('bar/123')
        self.assertIsNotNone(variables)
        self.assertEquals(variables['foo'], '123')

    def test_should_not_match_a_path_with_an_int_variable(self):
        variables = Path.parse('bar/{foo:int}').accept('bar/aaa')
        self.assertIsNone(variables)

    def test_should_not_match_a_path_with_a_path_variable(self):
        variables = Path.parse('bar/{foo:path}/c').accept('bar/a/b/c')

        self.assertIsNotNone(variables)
        self.assertEquals(variables['foo'], 'a/b')

    def test_should_not_match_a_path_with_special_characters(self):
        variables = Path.parse('bar/$[a-A]').accept('bar/$[a-A]')

        self.assertIsNotNone(variables)


def suite():
    aSuite = unittest.TestSuite()
    aSuite.addTest(unittest.makeSuite(TestCase))
    return aSuite


if __name__ == '__main__':
    unittest.main()
