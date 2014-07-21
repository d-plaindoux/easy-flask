import unittest
import suites

if __name__ == '__main__':
    suite = unittest.TestSuite()
    suite.addTest(suites.fluent_rest.verb.suite())
    suite.addTest(suites.fluent_rest.path.suite())
    suite.addTest(suites.fluent_rest.mime.suite())
    unittest.TextTestRunner(verbosity=2).run(suite)
