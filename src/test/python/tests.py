import unittest
import suites

if __name__ == '__main__':
    suite = unittest.TestSuite()
    suite.addTest(suites.fluent_rest.spec.path_parse.suite())
    suite.addTest(suites.fluent_rest.spec.path_match.suite())
    suite.addTest(suites.fluent_rest.spec.verb.suite())
    suite.addTest(suites.fluent_rest.spec.mime.suite())
    suite.addTest(suites.fluent_rest.inspector.inspection.suite())
    unittest.TextTestRunner(verbosity=2).run(suite)
