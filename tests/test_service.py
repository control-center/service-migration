import unittest
import os

import servicemigration as sm
sm.require(sm.version.API_VERSION)

INFILENAME = os.path.join(os.path.dirname(__file__), "v1.0.0.json")
OUTFILENAME = os.path.join(os.path.dirname(__file__), "out.json")

class ServiceTest(unittest.TestCase):

    def test_description_remove(self):
        """
        Tests completely removing a description.
        """
        ctx = sm.ServiceContext(INFILENAME)
        svc = filter(lambda x: x.description == "Zope server", ctx.services)[0]
        svc.description = None
        ctx.commit(OUTFILENAME)
        ctx = sm.ServiceContext(OUTFILENAME)
        svc = filter(lambda x: x.description == None, ctx.services)
        self.assertEqual(len(svc), 1)

    def test_description_change(self):
        """
        Tests altering a description.
        """
        ctx = sm.ServiceContext(INFILENAME)
        svc = filter(lambda x: x.description == "Zope server", ctx.services)[0]
        svc.description = "an_unlikely-description"
        ctx.commit(OUTFILENAME)
        ctx = sm.ServiceContext(OUTFILENAME)
        svc = filter(lambda x: x.description == "an_unlikely-description", ctx.services)
        self.assertEqual(len(svc), 1)

    def test_startup_remove(self):
        """
        Tests completely removing a startup.
        """
        ctx = sm.ServiceContext(INFILENAME)
        svc = filter(lambda x: x.description == "Zope server", ctx.services)[0]
        svc.startup = None
        ctx.commit(OUTFILENAME)
        ctx = sm.ServiceContext(OUTFILENAME)
        svc = filter(lambda x: x.startup == None, ctx.services)
        self.assertEqual(len(svc), 1)

    def test_startup_change(self):
        """
        Tests altering a startup.
        """
        ctx = sm.ServiceContext(INFILENAME)
        svc = filter(lambda x: x.description == "Zope server", ctx.services)[0]
        svc.startup = "an_unlikely-startup"
        ctx.commit(OUTFILENAME)
        ctx = sm.ServiceContext(OUTFILENAME)
        svc = filter(lambda x: x.startup == "an_unlikely-startup", ctx.services)
        self.assertEqual(len(svc), 1)

    def test_runs_remove(self):
        """
        Tests removing specific runs.
        """
        ctx = sm.ServiceContext(INFILENAME)
        svc = filter(lambda x: x.description == "Zope server", ctx.services)[0]
        self.assertEqual(len(svc.runs), 7)
        svc.runs = filter(lambda r: r.name != "apply-custom-patches", svc.runs)
        svc.runs = filter(lambda r: r.name != "help", svc.runs)
        ctx.commit(OUTFILENAME)
        ctx = sm.ServiceContext(OUTFILENAME)
        svc = filter(lambda x: x.description == "Zope server", ctx.services)[0]
        self.assertEqual(len(svc.runs), 5)
        for run in svc.runs:
            if run.name in ["help", "apply-custom-patches"]:
                raise ValueError("Error removing run.")

    def test_runs_add(self):
        """
        Tests adding runs to an existing list.
        """
        ctx = sm.ServiceContext(INFILENAME)
        svc = filter(lambda x: x.description == "Zope server", ctx.services)[0]
        self.assertEqual(len(svc.runs), 7)
        svc.runs.append(sm.Run("foo", "bar"))
        svc.runs.append(sm.Run("bar", "baz"))
        ctx.commit(OUTFILENAME)
        ctx = sm.ServiceContext(OUTFILENAME)
        svc = filter(lambda x: x.description == "Zope server", ctx.services)[0]
        if not "foo" in [run.name for run in svc.runs]:
            raise ValueError("Failed to alter runs.")
        if not "bar" in [run.name for run in svc.runs]:
            raise ValueError("Failed to alter runs.")
        for run in svc.runs:
            if run.name == "foo":
                self.assertEqual(run.command, "bar")
            if run.name == "bar":
                self.assertEqual(run.command, "baz")
        self.assertEqual(len(svc.runs), 9)

    def test_runs_replace(self):
        """
        Tests completely replacing the runs list.
        """
        ctx = sm.ServiceContext(INFILENAME)
        svc = filter(lambda x: x.description == "Zope server", ctx.services)[0]
        svc.runs = [
            sm.Run("foo", "bar"),            
            sm.Run("bar", "baz"),            
        ]
        ctx.commit(OUTFILENAME)
        ctx = sm.ServiceContext(OUTFILENAME)
        svc = filter(lambda x: x.description == "Zope server", ctx.services)[0]
        if not "foo" in [run.name for run in svc.runs]:
            raise ValueError("Failed to alter runs.")
        if not "bar" in [run.name for run in svc.runs]:
            raise ValueError("Failed to alter runs.")
        for run in svc.runs:
            if run.name == "foo":
                self.assertEqual(run.command, "bar")
            if run.name == "bar":
                self.assertEqual(run.command, "baz")
        self.assertEqual(len(svc.runs), 2)

    def test_endpoints_remove(self):
        """
        Tests removing specific endpoints.
        """
        ctx = sm.ServiceContext(INFILENAME)
        svc = filter(lambda x: x.description == "Zope server", ctx.services)[0]
        self.assertEqual(len(svc.endpoints), 9)
        svc.endpoints = filter(lambda r: r.name not in ["zenhub", "mariadb"], svc.endpoints)
        ctx.commit(OUTFILENAME)
        ctx = sm.ServiceContext(OUTFILENAME)
        svc = filter(lambda x: x.description == "Zope server", ctx.services)[0]
        self.assertEqual(len(svc.endpoints), 7)
        for ep in svc.endpoints:
            if ep.name in ["zenhub", "mariadb"]:
                raise ValueError("Error removing endpoint.")

    def test_endpoints_add(self):
        """
        Tests adding endpoints to an existing list.
        """
        ctx = sm.ServiceContext(INFILENAME)
        svc = filter(lambda x: x.description == "Zope server", ctx.services)[0]
        self.assertEqual(len(svc.endpoints), 9)
        svc.endpoints.append(sm.Endpoint("foo", "bar"))
        svc.endpoints.append(sm.Endpoint("bar", "baz"))
        ctx.commit(OUTFILENAME)
        ctx = sm.ServiceContext(OUTFILENAME)
        svc = filter(lambda x: x.description == "Zope server", ctx.services)[0]
        if not "foo" in [ep.name for ep in svc.endpoints]:
            raise ValueError("Failed to alter endpoints.")
        if not "bar" in [ep.name for ep in svc.endpoints]:
            raise ValueError("Failed to alter endpoints.")
        for ep in svc.endpoints:
            if ep.name == "foo":
                self.assertEqual(ep.purpose, "bar")
            if ep.name == "bar":
                self.assertEqual(ep.purpose, "baz")
        self.assertEqual(len(svc.endpoints), 11)

    def test_endpoints_replace(self):
        """
        Tests completely replacing the endpoints list.
        """
        ctx = sm.ServiceContext(INFILENAME)
        svc = filter(lambda x: x.description == "Zope server", ctx.services)[0]
        svc.endpoints = [
            sm.Endpoint("foo", "bar"),            
            sm.Endpoint("bar", "baz"),            
        ]
        ctx.commit(OUTFILENAME)
        ctx = sm.ServiceContext(OUTFILENAME)
        svc = filter(lambda x: x.description == "Zope server", ctx.services)[0]
        if not "foo" in [ep.name for ep in svc.endpoints]:
            raise ValueError("Failed to alter endpoints.")
        if not "bar" in [ep.name for ep in svc.endpoints]:
            raise ValueError("Failed to alter endpoints.")
        for ep in svc.endpoints:
            if ep.name == "foo":
                self.assertEqual(ep.purpose, "bar")
            if ep.name == "bar":
                self.assertEqual(ep.purpose, "baz")
        self.assertEqual(len(svc.endpoints), 2)

    def test_volumes_remove(self):
        """
        Tests removing specific volumes.
        """
        ctx = sm.ServiceContext(INFILENAME)
        svc = filter(lambda x: x.description == "Zope server", ctx.services)[0]
        self.assertEqual(len(svc.volumes), 8)
        svc.volumes = filter(lambda r: r.resourcePath not in ["zenjobs", "zenoss-export"], svc.volumes)
        ctx.commit(OUTFILENAME)
        ctx = sm.ServiceContext(OUTFILENAME)
        svc = filter(lambda x: x.description == "Zope server", ctx.services)[0]
        self.assertEqual(len(svc.volumes), 6)
        for v in svc.volumes:
            if v.resourcePath in ["zenjobs", "zenoss-export"]:
                raise ValueError("Error removing volume.")

    def test_volumes_add(self):
        """
        Tests adding volumes to an existing list.
        """
        ctx = sm.ServiceContext(INFILENAME)
        svc = filter(lambda x: x.description == "Zope server", ctx.services)[0]
        self.assertEqual(len(svc.volumes), 8)
        svc.volumes.append(sm.Volume("foo", "bar"))
        svc.volumes.append(sm.Volume("bar", "baz"))
        ctx.commit(OUTFILENAME)
        ctx = sm.ServiceContext(OUTFILENAME)
        svc = filter(lambda x: x.description == "Zope server", ctx.services)[0]
        if not "foo" in [v.owner for v in svc.volumes]:
            raise ValueError("Failed to alter volumes.")
        if not "bar" in [v.owner for v in svc.volumes]:
            raise ValueError("Failed to alter volumes.")
        for v in svc.volumes:
            if v.owner == "foo":
                self.assertEqual(v.permission, "bar")
            if v.owner == "bar":
                self.assertEqual(v.permission, "baz")
        self.assertEqual(len(svc.volumes), 10)

    def test_volumes_replace(self):
        """
        Tests completely replacing the volumes list.
        """
        ctx = sm.ServiceContext(INFILENAME)
        svc = filter(lambda x: x.description == "Zope server", ctx.services)[0]
        svc.volumes = [
            sm.Volume("foo", "bar"),            
            sm.Volume("bar", "baz"),            
        ]
        ctx.commit(OUTFILENAME)
        ctx = sm.ServiceContext(OUTFILENAME)
        svc = filter(lambda x: x.description == "Zope server", ctx.services)[0]
        if not "foo" in [v.owner for v in svc.volumes]:
            raise ValueError("Failed to alter volumes.")
        if not "bar" in [v.owner for v in svc.volumes]:
            raise ValueError("Failed to alter volumes.")
        for v in svc.volumes:
            if v.owner == "foo":
                self.assertEqual(v.permission, "bar")
            if v.owner == "bar":
                self.assertEqual(v.permission, "baz")
        self.assertEqual(len(svc.volumes), 2)

    def test_healthchecks_remove(self):
        """
        Tests removing specific healthchecks.
        """
        ctx = sm.ServiceContext(INFILENAME)
        svc = filter(lambda x: x.description == "Zope server", ctx.services)[0]
        self.assertEqual(len(svc.healthChecks), 7)
        svc.healthChecks = filter(lambda r: r.name not in ["answering", "running"], svc.healthChecks)
        ctx.commit(OUTFILENAME)
        ctx = sm.ServiceContext(OUTFILENAME)
        svc = filter(lambda x: x.description == "Zope server", ctx.services)[0]
        self.assertEqual(len(svc.healthChecks), 5)
        for hc in svc.healthChecks:
            if hc.name in ["answering", "running"]:
                raise ValueError("Error removing healthcheck.")

    def test_healthchecks_add(self):
        """
        Tests adding healthchecks to an existing list.
        """
        ctx = sm.ServiceContext(INFILENAME)
        svc = filter(lambda x: x.description == "Zope server", ctx.services)[0]
        self.assertEqual(len(svc.healthChecks), 7)
        svc.healthChecks.append(sm.HealthCheck("foo", "bar"))
        svc.healthChecks.append(sm.HealthCheck("bar", "baz"))
        ctx.commit(OUTFILENAME)
        ctx = sm.ServiceContext(OUTFILENAME)
        svc = filter(lambda x: x.description == "Zope server", ctx.services)[0]
        if not "foo" in [hc.name for hc in svc.healthChecks]:
            raise ValueError("Failed to alter healthchecks.")
        if not "bar" in [hc.name for hc in svc.healthChecks]:
            raise ValueError("Failed to alter healthchecks.")
        for hc in svc.healthChecks:
            if hc.name == "foo":
                self.assertEqual(hc.script, "bar")
            if hc.name == "bar":
                self.assertEqual(hc.script, "baz")
        self.assertEqual(len(svc.healthChecks), 9)

    def test_healthchecks_replace(self):
        """
        Tests completely replacing the healthchecks list.
        """
        ctx = sm.ServiceContext(INFILENAME)
        svc = filter(lambda x: x.description == "Zope server", ctx.services)[0]
        svc.healthChecks = [
            sm.HealthCheck("foo", "bar"),            
            sm.HealthCheck("bar", "baz"),            
        ]
        ctx.commit(OUTFILENAME)
        ctx = sm.ServiceContext(OUTFILENAME)
        svc = filter(lambda x: x.description == "Zope server", ctx.services)[0]
        if not "foo" in [hc.name for hc in svc.healthChecks]:
            raise ValueError("Failed to alter healthchecks.")
        if not "bar" in [hc.name for hc in svc.healthChecks]:
            raise ValueError("Failed to alter healthchecks.")
        for hc in svc.healthChecks:
            if hc.name == "foo":
                self.assertEqual(hc.script, "bar")
            if hc.name == "bar":
                self.assertEqual(hc.script, "baz")
        self.assertEqual(len(svc.healthChecks), 2)

    def test_instancelimits_change(self):
        """
        Tests changing the instance limits.
        """
        ctx = sm.ServiceContext(INFILENAME)
        svc = filter(lambda x: x.description == "Zope server", ctx.services)[0]
        svc.instanceLimits.minimum = 123
        svc.instanceLimits.maximum = 1234
        svc.instanceLimits.default = 234
        ctx.commit(OUTFILENAME)
        ctx = sm.ServiceContext(OUTFILENAME)
        svc = filter(lambda x: x.description == "Zope server", ctx.services)[0]
        self.assertEqual(svc.instanceLimits.minimum, 123)
        self.assertEqual(svc.instanceLimits.maximum, 1234)
        self.assertEqual(svc.instanceLimits.default, 234)

    def test_desiredState(self):
        """
        Tests changing the desired state.
        """
        ctx = sm.ServiceContext(INFILENAME)
        svc = filter(lambda x: x.name == "redis", ctx.services)[0]
        svc.desiredState = sm.RESTART
        ctx.commit(OUTFILENAME)
        ctx = sm.ServiceContext(OUTFILENAME)
        svc = filter(lambda x: x.name == "redis", ctx.services)[0]
        self.assertEqual(svc.desiredState, sm.RESTART)

    def test_configfiles_remove(self):
        """
        Tests removing specific config files.
        """
        ctx = sm.ServiceContext(INFILENAME)
        svc = filter(lambda x: x.description == "Zope server", ctx.services)[0]
        self.assertEqual(len(svc.configFiles), 2)
        svc.configFiles = filter(lambda r: r.name not in ["/opt/zenoss/etc/global.conf"], svc.configFiles)
        ctx.commit(OUTFILENAME)
        ctx = sm.ServiceContext(OUTFILENAME)
        svc = filter(lambda x: x.description == "Zope server", ctx.services)[0]
        self.assertEqual(len(svc.configFiles), 1)
        for cf in svc.configFiles:
            if cf.name == "/opt/zenoss/etc/global.conf":
                raise ValueError("Error removing config file.")

    def test_configfiles_add(self):
        """
        Tests adding config files to an existing list.
        """
        ctx = sm.ServiceContext(INFILENAME)
        svc = filter(lambda x: x.description == "Zope server", ctx.services)[0]
        self.assertEqual(len(svc.configFiles), 2)
        svc.configFiles.append(sm.ConfigFile("foo", "bar", "baz", 777, "foo bar baz"))
        svc.configFiles.append(sm.ConfigFile("baz", "foo", "bar", 111, "baz foo bar"))
        ctx.commit(OUTFILENAME)
        ctx = sm.ServiceContext(OUTFILENAME)
        svc = filter(lambda x: x.description == "Zope server", ctx.services)[0]
        if not "foo" in [hc.name for hc in svc.configFiles]:
            raise ValueError("Failed to alter configFiles.")
        if not "baz" in [hc.name for hc in svc.configFiles]:
            raise ValueError("Failed to alter configFiles.")
        for cf in svc.configFiles:
            if cf.name == "foo":
                self.assertEqual(cf.content, "foo bar baz")
            if cf.name == "baz":
                self.assertEqual(cf.permissions, 111)
        self.assertEqual(len(svc.configFiles), 4)

    def test_configfiles_replace(self):
        """
        Tests completely replacing the configfiles list.
        """
        ctx = sm.ServiceContext(INFILENAME)
        svc = filter(lambda x: x.description == "Zope server", ctx.services)[0]
        svc.configFiles = [
            sm.ConfigFile("foo", "bar", "baz", 777, "foo bar baz"),
            sm.ConfigFile("baz", "foo", "bar", 111, "baz foo bar")
        ]
        ctx.commit(OUTFILENAME)
        ctx = sm.ServiceContext(OUTFILENAME)
        svc = filter(lambda x: x.description == "Zope server", ctx.services)[0]
        if not "foo" in [cf.name for cf in svc.configFiles]:
            raise ValueError("Failed to alter config files.")
        if not "baz" in [cf.name for cf in svc.configFiles]:
            raise ValueError("Failed to alter config files.")
        for cf in svc.configFiles:
            if cf.name == "foo":
                self.assertEqual(cf.content, "foo bar baz")
            if cf.name == "baz":
                self.assertEqual(cf.permissions, 111)
        self.assertEqual(len(svc.configFiles), 2)
