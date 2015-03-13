import unittest
import os

import servicemigration as sm
sm.require(sm.version.API_VERSION)

INFILENAME = os.path.join(os.path.dirname(__file__), "v1.0.0.json")
OUTFILENAME = os.path.join(os.path.dirname(__file__), "out.json")

class ServiceTest(unittest.TestCase):

    def test_get_commit_services(self):
        """
        Tests ServiceContext creation and commit.
        """
        ctx = sm.ServiceContext(INFILENAME)
        self.assertEqual(len(ctx.services), 33)
        ctx.services.pop()
        self.assertEqual(len(ctx.services), 32)
        ctx.commit(OUTFILENAME)
        ctx = sm.ServiceContext(OUTFILENAME)
        self.assertEqual(len(ctx.services), 32)


