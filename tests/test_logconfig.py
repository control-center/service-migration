import unittest
import os

import servicemigration as sm
sm.require(sm.version.API_VERSION)

INFILENAME = os.path.join(os.path.dirname(__file__), "v1.0.0.json")
OUTFILENAME = os.path.join(os.path.dirname(__file__), "out.json")

class LogConfigTest(unittest.TestCase):

    def tests_logconfigs_add(self):
        """
        Tests adding a new file to a service's LogConfigs.
        """
        ctx = sm.ServiceContext(INFILENAME)
        svc = filter(lambda x: x.description == "Zope server", ctx.services)[0]
        self.assertEqual(len(svc.logConfigs), 3)
        svc.logConfigs.append(
                sm.LogConfig(path="/opt/zenoss/log/honk.log", logType="honk"))
        ctx.commit(OUTFILENAME)
        ctx = sm.ServiceContext(OUTFILENAME)
        svc = filter(lambda x: x.description == "Zope server", ctx.services)[0]

        if not "honk" in [hc.logType for hc in svc.logConfigs]:
            raise ValueError("Failed to alter logconfigs.")
        for lc in svc.logConfigs:
            if lc.logType == "honk":
                self.assertEqual(lc.path, "/opt/zenoss/log/honk.log")
                self.assertEqual(lc.isAudit, False)
        self.assertEqual(len(svc.logConfigs), 4)

    def tests_logconfigs_remove(self):
        """
        Tests removing a file from a service's LogConfigs.
        """
        ctx = sm.ServiceContext(INFILENAME)
        svc = filter(lambda x: x.description == "Zope server", ctx.services)[0]
        self.assertEqual(len(svc.logConfigs), 3)

        no_audits = filter(lambda x: x.logType != 'zenossaudit', svc.logConfigs)
        self.assertEqual(len(no_audits), 2)
        svc.logConfigs = no_audits

        ctx.commit(OUTFILENAME)
        ctx = sm.ServiceContext(OUTFILENAME)
        svc = filter(lambda x: x.description == "Zope server", ctx.services)[0]

        if "zenossaudit" in [hc.logType for hc in svc.logConfigs]:
            raise ValueError("Failed to alter logconfigs.")
        self.assertEqual(len(svc.logConfigs), 2)

    def tests_logconfigs_alter(self):
        """
        Tests changing the LogConfigs of a service.
        """
        ctx = sm.ServiceContext(INFILENAME)
        svc = filter(lambda x: x.description == "Zope server", ctx.services)[0]
        self.assertEqual(len(svc.logConfigs), 3)
        for lc in svc.logConfigs:
            if lc.logType == 'zenossaudit':
                # Add or update logtag "foo" to "bar".
                for tag in lc.logTags:
                    if tag.name == 'foo':
                        tag.value = 'bar'
                        break
                else:
                    lc.logTags.append(sm.logtag.LogTag(name="foo", value="bar"))
                lc.filters.append('baz')

        svc = filter(lambda x: x.description == "Zope server", ctx.services)[0]

        audit = filter(lambda x: x.logType == 'zenossaudit', svc.logConfigs)[0]
        footags = filter(lambda t: t.name == 'foo', audit.logTags)
        self.assertEqual(len(footags), 1)
        self.assertEqual(footags[0].value, 'bar', "Failed ot alter logconfigs.")
        self.assertTrue('baz' in audit.filters, "Failed to alter logconfigs.")
        self.assertEqual(len(svc.logConfigs), 3)

    def test_isAudit_change(self):
        """
        Tests changing the IsAudit property
        """

        ctx = sm.ServiceContext(INFILENAME)
        svc = filter(lambda x: x.description == "Zope server", ctx.services)[0]

        # The default value is True
        for lc in svc.logConfigs:
            self.assertEqual(lc.isAudit, False)

        svc.logConfigs[0].isAudit = True
        ctx.commit(OUTFILENAME)

        ctx = sm.ServiceContext(OUTFILENAME)
        svc = filter(lambda x: x.description == "Zope server", ctx.services)[0]
        self.assertEqual(svc.logConfigs[0].isAudit, True)
        self.assertEqual(svc.logConfigs[1].isAudit, False)
        self.assertEqual(svc.logConfigs[2].isAudit, False)
