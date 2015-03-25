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

    def test_ctx_versioning(self):
        """
        Tests ServiceContext versioning
        """
        ctx = sm.ServiceContext(INFILENAME)
        ctx.version = "foo.bar.baz"
        ctx.commit(OUTFILENAME)
        ctx = sm.ServiceContext(OUTFILENAME)
        self.assertEqual(ctx.version, "foo.bar.baz")

    def test_sdk_versioning_major_big(self):
        major = int(sm.version.API_VERSION.split('.')[0]) + 1
        minor = int(sm.version.API_VERSION.split('.')[1])
        bugfx = int(sm.version.API_VERSION.split('.')[2])
        try:
            sm.require("%d.%d.%d" % (major, minor, bugfx))
        except ValueError:
            return
        raise ValueError("SDK Versioning logic failed.")

    def test_sdk_versioning_major_small(self):
        major = int(sm.version.API_VERSION.split('.')[0]) - 1
        minor = int(sm.version.API_VERSION.split('.')[1])
        bugfx = int(sm.version.API_VERSION.split('.')[2])
        try:
            sm.require("%d.%d.%d" % (major, minor, bugfx))
        except ValueError:
            return
        raise ValueError("SDK Versioning logic failed.")

    def test_sdk_versioning_minor_big(self):
        major = int(sm.version.API_VERSION.split('.')[0])
        minor = int(sm.version.API_VERSION.split('.')[1]) + 1
        bugfx = int(sm.version.API_VERSION.split('.')[2])
        try:
            sm.require("%d.%d.%d" % (major, minor, bugfx))
        except ValueError:
            return
        raise ValueError("SDK Versioning logic failed.")

    def test_sdk_versioning_minor_small(self):
        major = int(sm.version.API_VERSION.split('.')[0])
        minor = int(sm.version.API_VERSION.split('.')[1]) - 1
        bugfx = int(sm.version.API_VERSION.split('.')[2])
        sm.require("%d.%d.%d" % (major, minor, bugfx))

    def test_sdk_versioning_bugfix_big(self):
        major = int(sm.version.API_VERSION.split('.')[0])
        minor = int(sm.version.API_VERSION.split('.')[1])
        bugfx = int(sm.version.API_VERSION.split('.')[2]) + 1
        try:
            sm.require("%d.%d.%d" % (major, minor, bugfx))
        except ValueError:
            return
        raise ValueError("SDK Versioning logic failed.")

    def test_sdk_versioning_bugfix_small(self):
        major = int(sm.version.API_VERSION.split('.')[0])
        minor = int(sm.version.API_VERSION.split('.')[1])
        bugfx = int(sm.version.API_VERSION.split('.')[2]) - 1
        sm.require("%d.%d.%d" % (major, minor, bugfx))

    def test_findService(self):
        ctx = sm.ServiceContext(INFILENAME)
        svc = ctx.findService("Zenoss.core/redis")
        self.assertEqual(svc.name, "redis")
        svc = ctx.findService("Zenoss.core/not-a-service")
        self.assertEqual(svc, None)

    def test_findServices(self):
        ctx = sm.ServiceContext(INFILENAME)
        svcs = ctx.findServices(r".*/localhost/localhost/.*")
        self.assertEqual(len(svcs), 13)
        for svc in svcs:
            self.assertEqual("/localhost/localhost" in svc.getPath(), True)
        svcs = ctx.findServices(r"Zenoss\.core")
        self.assertEqual(len(svcs), 33)
        svcs = ctx.findServices(r".*redis$")
        self.assertEqual(len(svcs), 2)
