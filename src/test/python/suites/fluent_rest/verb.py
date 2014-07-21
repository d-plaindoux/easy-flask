import unittest
from fluent_rest.rest import *
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

        self.assertTrue(specs(test).hasVerb(u'GET'))

    def test_should_have_PUT(self):
        @PUT
        def test():
            pass

        self.assertTrue(specs(test).hasVerb(u'PUT'))

    def test_should_have_POST(self):
        @POST
        def test():
            pass

        self.assertTrue(specs(test).hasVerb(u'POST'))

    def test_should_have_DELETE(self):
        @DELETE
        def test():
            pass

        self.assertTrue(specs(test).hasVerb(u'DELETE'))

    def test_should_have_a_Verb(self):
        @Verb(u'UPLOAD')
        def test():
            pass

        self.assertTrue(specs(test).hasVerb(u'UPLOAD'))

    def test_should_not_have_GET_and_PUT(self):
        try:
            @GET
            @PUT
            def test_function_to_be_rejected():
                pass

            self.fail('Cannot have more than one verb')
        except OverloadedVerbException, _:
            pass


def suite():
    aSuite = unittest.TestSuite()
    aSuite.addTest(unittest.makeSuite(TestCase))
    return aSuite


if __name__ == '__main__':
    unittest.main()
