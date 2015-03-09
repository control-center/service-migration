import unittest
import os

import servicemigration as sm
sm.require(sm.version.API_VERSION)

INFILENAME = os.path.join(os.path.dirname(__file__), "v1.0.0.json")
OUTFILENAME = os.path.join(os.path.dirname(__file__), "out.json")

class ServiceTest(unittest.TestCase):

    def test_get_services(self):
        ctx = sm.ServiceContext(INFILENAME)

    def test_commit(self):
        ctx = sm.ServiceContext(INFILENAME)
        ctx.services[0].description = "an_unlikely-description"
        ctx.services[0].runs["foo"] = "bar"
        ctx.commit(OUTFILENAME)
        ctx = sm.ServiceContext(OUTFILENAME)
        result = filter(lambda x: x.description == "an_unlikely-description", ctx.services)
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0].description, "an_unlikely-description")
        self.assertEqual(result[0].runs["foo"], "bar")
