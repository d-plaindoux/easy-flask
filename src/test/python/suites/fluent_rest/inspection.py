import unittest
from fluent_rest.rest import *
from fluent_rest.inspection import inspect
from fluent_rest.exceptions import OverloadedPathException


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

        self.assertEquals(inspect(test).handle(lambda f: f), [test])

    def test_should_inspect_class(self):
        class Test:
            def __init__(self):
                pass

            @GET
            @Path('bar')
            @Consumes('application/json')
            def test(self):
                pass

        self.assertEquals(inspect(Test).handle(lambda f: f), [Test.test])

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

        self.assertEquals(inspect(Test).handle(lambda f: f), [Test.test])
        self.assertEquals(specs(Test.test).getPath(), 'foo/bar')

    def test_should_inspect_specified_class_adding_path(self):
        @Path('foo')
        class Test:
            def __init__(self):
                pass

            @GET
            @Consumes('application/json')
            def test(self):
                pass

        self.assertEquals(inspect(Test).handle(lambda f: f), [Test.test])
        self.assertEquals(specs(Test.test).getPath(), 'foo')

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

        self.assertEquals(inspect(Test).handle(lambda f: f), [Test.test])
        self.assertTrue(specs(Test.test).hasGivenConsumes('application/json'))

    def test_should_inspect_specified_adding_produces(self):
        @Path('foo')
        @Produces('application/json')
        class Test:
            def __init__(self):
                pass

            @GET
            def test(self):
                pass

        self.assertEquals(inspect(Test).handle(lambda f: f), [Test.test])
        self.assertTrue(specs(Test.test).hasGivenProduces('application/json'))


def suite():
    aSuite = unittest.TestSuite()
    aSuite.addTest(unittest.makeSuite(TestCase))
    return aSuite


if __name__ == '__main__':
    unittest.main()
