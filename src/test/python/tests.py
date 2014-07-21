import unittest
import suites

if __name__ == '__main__':
    suite = unittest.TestSuite()
    suite.addTest(suites.easy_rest.verb.suite())
    suite.addTest(suites.easy_rest.path.suite())
    suite.addTest(suites.easy_rest.mime.suite())
    unittest.TextTestRunner(verbosity=2).run(suite)
