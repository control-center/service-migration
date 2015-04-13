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
            self.assertEqual("/localhost/localhost" in ctx.getServicePath(svc), True)
        svcs = ctx.findServices(r"Zenoss\.core")
        self.assertEqual(len(svcs), 33)
        svcs = ctx.findServices(r".*redis$")
        self.assertEqual(len(svcs), 2)

    def test_getServicePath(self):
        ctx = sm.ServiceContext(INFILENAME)
        svc = filter(lambda x: x.name == "collectorredis", ctx.services)[0]
        self.assertEqual(ctx.getServicePath(svc), "Zenoss.core/localhost/localhost/collectorredis")
        svc = filter(lambda x: x.name == "Zenoss.core", ctx.services)[0]
        self.assertEqual(ctx.getServicePath(svc), "Zenoss.core")

    def test_reparentService_tenant(self):
        ctx = sm.ServiceContext(INFILENAME)
        svc0 = filter(lambda x: x.name == "Zenoss.core", ctx.services)[0]
        svc1 = filter(lambda x: x.name == "collectorredis", ctx.services)[0]
        try:
            ctx.reparentService(svc0, svc1)
        except ValueError as e:
            self.assertEqual(str(e), "Can't reparent tenant.")
            return
        raise ValueError("Should not be able to reparent the tenant.")

    def test_reparentService_cycle(self):
        ctx = sm.ServiceContext(INFILENAME)
        svc0 = filter(lambda x: x.name == "localhost", ctx.services)[0]
        svc1 = filter(lambda x: x.name == "collectorredis", ctx.services)[0]
        try:
            ctx.reparentService(svc0, svc1)
        except ValueError as e:
            self.assertEqual(str(e), "Cycle detected in service tree.")
            return
        raise ValueError("Failed to detect cycle in service tree.")

    def test_reparentService(self):
        ctx = sm.ServiceContext(INFILENAME)
        svc0 = filter(lambda x: x.name == "collectorredis", ctx.services)[0]
        svc1 = filter(lambda x: x.name == "redis", ctx.services)[0]
        ctx.reparentService(svc0, svc1)
        ctx.commit(OUTFILENAME)
        ctx = sm.ServiceContext(OUTFILENAME)
        svc0 = filter(lambda x: x.name == "collectorredis", ctx.services)[0]
        svc1 = filter(lambda x: x.name == "redis", ctx.services)[0]
        self.assertEqual(ctx.getServiceParent(svc0), svc1)
        self.assertTrue(svc0 in ctx.getServiceChildren(svc1))

    def test_getServiceChildren(self):
        ctx = sm.ServiceContext(INFILENAME)
        svc = filter(lambda x: x.name == "Zenoss.core", ctx.services)[0]
        self.assertEqual(len(ctx.getServiceChildren(svc)), 14)

    def test_getServiceParent(self):
        ctx = sm.ServiceContext(INFILENAME)
        svc = filter(lambda x: x.name == "redis", ctx.services)[0]
        self.assertEqual(ctx.getServiceParent(svc).name, "Zenoss.core")

    def test_cloneService(self):
        ctx = sm.ServiceContext(INFILENAME)
        redis = filter(lambda x: x.name == "redis", ctx.services)[0]
        clone = ctx.cloneService(redis)
        clone.name = "clone name"
        ctx.commit(OUTFILENAME)
        ctx = sm.ServiceContext(OUTFILENAME)
        clone = filter(lambda x: x.name == "clone name", ctx.services)[0]
        self.assertEqual(clone.description, redis.description)
