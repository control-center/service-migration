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

    def test_commands_remove(self):
        """
        Tests removing specific commands.
        """
        ctx = sm.ServiceContext(INFILENAME)
        svc = filter(lambda x: x.description == "Zope server", ctx.services)[0]
        self.assertEqual(len(svc.commands), 8)
        svc.commands = filter(lambda r: r.name != "apply-custom-patches", svc.commands)
        svc.commands = filter(lambda r: r.name != "help", svc.commands)
        ctx.commit(OUTFILENAME)
        ctx = sm.ServiceContext(OUTFILENAME)
        svc = filter(lambda x: x.description == "Zope server", ctx.services)[0]
        self.assertEqual(len(svc.commands), 6)
        for command in svc.commands:
            if command.name in ["help", "apply-custom-patches"]:
                raise ValueError("Error removing command.")

    def test_commands_add(self):
        """
        Tests adding commands to an existing list.
        """
        ctx = sm.ServiceContext(INFILENAME)
        svc = filter(lambda x: x.description == "Zope server", ctx.services)[0]
        self.assertEqual(len(svc.commands), 8)
        svc.commands.append(sm.Command("foo", "bar", commitOnSuccess=False,
                                        description="Description of foo bar"))
        svc.commands.append(sm.Command("bar", "baz", commitOnSuccess=True,
                                       description="Description of bar baz"))
        ctx.commit(OUTFILENAME)
        ctx = sm.ServiceContext(OUTFILENAME)
        svc = filter(lambda x: x.description == "Zope server", ctx.services)[0]
        if not "foo" in [command.name for command in svc.commands]:
            raise ValueError("Failed to alter commands.")
        if not "bar" in [command.name for command in svc.commands]:
            raise ValueError("Failed to alter commands.")
        for command in svc.commands:
            if command.name == "foo":
                self.assertEqual(command.command, "bar")
                self.assertEqual(command.description, "Description of foo bar")
                self.assertFalse(command.commitOnSuccess)
            if command.name == "bar":
                self.assertEqual(command.command, "baz")
                self.assertEqual(command.description, "Description of bar baz")
                self.assertTrue(command.commitOnSuccess)
        self.assertEqual(len(svc.commands), 10)

    def test_commands_replace(self):
        """
        Tests completely replacing the commands list.
        """
        ctx = sm.ServiceContext(INFILENAME)
        svc = filter(lambda x: x.description == "Zope server", ctx.services)[0]
        svc.commands = [
            sm.Command("foo", "bar", commitOnSuccess=False),
            sm.Command("bar", "baz", commitOnSuccess=True),
        ]
        ctx.commit(OUTFILENAME)
        ctx = sm.ServiceContext(OUTFILENAME)
        svc = filter(lambda x: x.description == "Zope server", ctx.services)[0]
        if not "foo" in [command.name for command in svc.commands]:
            raise ValueError("Failed to alter commands.")
        if not "bar" in [command.name for command in svc.commands]:
            raise ValueError("Failed to alter commands.")
        for command in svc.commands:
            if command.name == "foo":
                self.assertEqual(command.command, "bar")
                self.assertFalse(command.commitOnSuccess)
            if command.name == "bar":
                self.assertEqual(command.command, "baz")
                self.assertTrue(command.commitOnSuccess)
        self.assertEqual(len(svc.commands), 2)

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

    def test_add_prereqs(self):
        # Reset
        ctx = sm.ServiceContext(INFILENAME)
        svc = filter(lambda x: x.name == "HMaster", ctx.services)[0]
        newPr = sm.Prereq("Andy", "TheCommand")
        svc.prereqs = [newPr]
        ctx.commit(OUTFILENAME)
        ctx = sm.ServiceContext(OUTFILENAME)
        svc = filter(lambda x: x.name == "HMaster", ctx.services)[0]
        self.assertEqual(len(svc.prereqs), 1)
        self.assertEqual(svc.prereqs[0].name, "Andy")
        self.assertEqual(svc.prereqs[0].script, "TheCommand")

        # Add one
        svc.prereqs.append(sm.Prereq("Bob", "ThatCommand"))
        ctx.commit(OUTFILENAME)
        ctx = sm.ServiceContext(OUTFILENAME)
        svc = filter(lambda x: x.name == "HMaster", ctx.services)[0]
        sortedPrereqs = sorted(svc.prereqs, key=lambda k: k.name)
        self.assertEqual(len(svc.prereqs), 2)
        self.assertEqual(sortedPrereqs[0].name, "Andy")
        self.assertEqual(sortedPrereqs[0].script, "TheCommand")
        self.assertEqual(sortedPrereqs[1].name, "Bob")
        self.assertEqual(sortedPrereqs[1].script, "ThatCommand")

    def test_modify_prereqs(self):
        # Modify
        ctx = sm.ServiceContext(INFILENAME)
        svc = filter(lambda x: x.name == "HMaster", ctx.services)[0]
        newPr = sm.Prereq("Andy", "TheCommand")
        svc.prereqs = [newPr]
        ctx.commit(OUTFILENAME)
        ctx = sm.ServiceContext(OUTFILENAME)
        svc = filter(lambda x: x.name == "HMaster", ctx.services)[0]
        svc.prereqs[0].name = "Alice"
        ctx.commit(OUTFILENAME)
        ctx = sm.ServiceContext(OUTFILENAME)
        svc = filter(lambda x: x.name == "HMaster", ctx.services)[0]
        self.assertEqual(len(svc.prereqs), 1)
        self.assertEqual(svc.prereqs[0].name, "Alice")
        self.assertEqual(svc.prereqs[0].script, "TheCommand")

        # Delete
        svc.prereqs = []
        ctx.commit(OUTFILENAME)
        ctx = sm.ServiceContext(OUTFILENAME)
        svc = filter(lambda x: x.name == "HMaster", ctx.services)[0]
        self.assertEqual(svc.prereqs, [])

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

    def test_originalconfigs_remove(self):
        """
        Tests removing specific config files.
        """
        ctx = sm.ServiceContext(INFILENAME)
        svc = filter(lambda x: x.description == "Zope server", ctx.services)[0]
        self.assertEqual(len(svc.originalConfigs), 2)
        svc.originalConfigs = filter(lambda r: r.name not in ["/opt/zenoss/etc/global.conf"], svc.originalConfigs)
        ctx.commit(OUTFILENAME)
        ctx = sm.ServiceContext(OUTFILENAME)
        svc = filter(lambda x: x.description == "Zope server", ctx.services)[0]
        self.assertEqual(len(svc.originalConfigs), 1)
        for cf in svc.originalConfigs:
            if cf.name == "/opt/zenoss/etc/global.conf":
                raise ValueError("Error removing config file.")

    def test_originalconfigs_add(self):
        """
        Tests adding config files to an existing list.
        """
        ctx = sm.ServiceContext(INFILENAME)
        svc = filter(lambda x: x.description == "Zope server", ctx.services)[0]
        self.assertEqual(len(svc.originalConfigs), 2)
        svc.originalConfigs.append(sm.ConfigFile("foo", "bar", "baz", "777", "foo bar baz"))
        svc.originalConfigs.append(sm.ConfigFile("baz", "foo", "bar", "111", "baz foo bar"))
        ctx.commit(OUTFILENAME)
        ctx = sm.ServiceContext(OUTFILENAME)
        svc = filter(lambda x: x.description == "Zope server", ctx.services)[0]
        if not "foo" in [hc.name for hc in svc.originalConfigs]:
            raise ValueError("Failed to alter originalConfigs.")
        if not "baz" in [hc.name for hc in svc.originalConfigs]:
            raise ValueError("Failed to alter originalConfigs.")
        for cf in svc.originalConfigs:
            if cf.name == "foo":
                self.assertEqual(cf.content, "foo bar baz")
            if cf.name == "baz":
                self.assertEqual(cf.permissions, "111")
        self.assertEqual(len(svc.originalConfigs), 4)

    def test_originalconfigs_replace(self):
        """
        Tests completely replacing the originalConfigs list.
        """
        ctx = sm.ServiceContext(INFILENAME)
        svc = filter(lambda x: x.description == "Zope server", ctx.services)[0]
        svc.originalConfigs = [
            sm.ConfigFile("foo", "bar", "baz", "777", "foo bar baz"),
            sm.ConfigFile("baz", "foo", "bar", "111", "baz foo bar")
        ]
        ctx.commit(OUTFILENAME)
        ctx = sm.ServiceContext(OUTFILENAME)
        svc = filter(lambda x: x.description == "Zope server", ctx.services)[0]
        if not "foo" in [cf.name for cf in svc.originalConfigs]:
            raise ValueError("Failed to alter config files.")
        if not "baz" in [cf.name for cf in svc.originalConfigs]:
            raise ValueError("Failed to alter config files.")
        for cf in svc.originalConfigs:
            if cf.name == "foo":
                self.assertEqual(cf.content, "foo bar baz")
            if cf.name == "baz":
                self.assertEqual(cf.permissions, "111")
        self.assertEqual(len(svc.originalConfigs), 2)

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
        svc.configFiles.append(sm.ConfigFile("foo", "bar", "baz", "777", "foo bar baz"))
        svc.configFiles.append(sm.ConfigFile("baz", "foo", "bar", "111", "baz foo bar"))
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
                self.assertEqual(cf.permissions, "111")
        self.assertEqual(len(svc.configFiles), 4)

    def test_configfiles_replace(self):
        """
        Tests completely replacing the configFiles list.
        """
        ctx = sm.ServiceContext(INFILENAME)
        svc = filter(lambda x: x.description == "Zope server", ctx.services)[0]
        svc.configFiles = [
            sm.ConfigFile("foo", "bar", "baz", "777", "foo bar baz"),
            sm.ConfigFile("baz", "foo", "bar", "111", "baz foo bar")
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
                self.assertEqual(cf.permissions, "111")
        self.assertEqual(len(svc.configFiles), 2)

    def test_metricconfig_remove(self):
        """
        Tests finding and removing a MetricConfig from a MonitoringProfile by ID.
        """
        ctx = sm.ServiceContext(INFILENAME)
        svc = filter(lambda x: x.name == "CentralQuery", ctx.services)[0]
        monpro = svc.monitoringProfile
        self.assertEqual(len(monpro.metricConfigs), 7)
        mc_ids = [mc.ID for mc in monpro.metricConfigs]
        self.assertEqual(len(mc_ids), 7)
        self.assertTrue('jvm.thread' in mc_ids)
        monpro.metricConfigs.pop(mc_ids.index('jvm.thread'))
        ctx.commit(OUTFILENAME)

        ctx = sm.ServiceContext(OUTFILENAME)
        svc = filter(lambda x: x.name == "CentralQuery", ctx.services)[0]
        monpro = svc.monitoringProfile
        self.assertEqual(len(monpro.metricConfigs), 6)
        mc_ids = [mc.ID for mc in monpro.metricConfigs]
        self.assertEqual(len(mc_ids), 6)
        self.assertTrue('jvm.thread' not in mc_ids)

    def test_metricconfig_add(self):
        """
        Tests creating and adding a new MetricConfig to a MonitoringProfile.
        """
        ctx = sm.ServiceContext(INFILENAME)
        svc = filter(lambda x: x.name == "CentralQuery", ctx.services)[0]
        monpro = svc.monitoringProfile
        self.assertEqual(len(monpro.metricConfigs), 7)

        mc = sm.monitoringprofile.metricconfig.MetricConfig(
            ID="foo", name="Foo", description="Test MC")
        monpro.metricConfigs.append(mc)

        ctx.commit(OUTFILENAME)

        ctx = sm.ServiceContext(OUTFILENAME)
        svc = filter(lambda x: x.name == "CentralQuery", ctx.services)[0]
        monpro = svc.monitoringProfile
        self.assertEqual(len(monpro.metricConfigs), 8)
        mc_ids = [mc.ID for mc in monpro.metricConfigs]
        self.assertEqual(len(mc_ids), 8)
        self.assertTrue('foo' in mc_ids)
        mc_foo = monpro.metricConfigs[mc_ids.index('foo')]
        self.assertEqual(mc_foo.ID, "foo")
        self.assertEqual(mc_foo.name, "Foo")
        self.assertEqual(mc_foo.description, "Test MC")
        self.assertEqual(mc_foo.metrics, [])

    def test_metricconfig_modify(self):
        """
        Tests finding MetricConfig in a MonitoringProfile by ID, and altering
        it in place.
        """
        ctx = sm.ServiceContext(INFILENAME)
        svc = filter(lambda x: x.name == "CentralQuery", ctx.services)[0]
        monpro = svc.monitoringProfile
        self.assertEqual(len(monpro.metricConfigs), 7)
        mc_ids = [mc.ID for mc in monpro.metricConfigs]
        self.assertEqual(len(mc_ids), 7)
        self.assertTrue('jvm.thread' in mc_ids)
        mc_jvmthread = monpro.metricConfigs[mc_ids.index('jvm.thread')]
        mc_jvmthread.description = "JVM Thread with a changed description"
        ctx.commit(OUTFILENAME)

        ctx = sm.ServiceContext(OUTFILENAME)
        svc = filter(lambda x: x.name == "CentralQuery", ctx.services)[0]
        monpro = svc.monitoringProfile
        self.assertEqual(len(monpro.metricConfigs), 7)
        mc_ids = [mc.ID for mc in monpro.metricConfigs]
        self.assertEqual(len(mc_ids), 7)
        self.assertTrue('jvm.thread' in mc_ids)
        mc_jvmthread = monpro.metricConfigs[mc_ids.index('jvm.thread')]
        self.assertEqual(mc_jvmthread.description, "JVM Thread with a changed description")

    def test_graphconfig_remove(self):
        """
        Tests finding and removing a GraphConfig from a MonitoringProfile by ID.
        """
        ctx = sm.ServiceContext(INFILENAME)
        svc = filter(lambda x: x.name == "collectorredis", ctx.services)[0]
        monpro = svc.monitoringProfile
        self.assertEqual(len(monpro.graphConfigs), 2)
        gc_ids = [gc.graphID for gc in monpro.graphConfigs]
        self.assertEqual(len(gc_ids), 2)
        self.assertTrue('metricqueue' in gc_ids)
        monpro.graphConfigs.pop(gc_ids.index('metricqueue'))
        ctx.commit(OUTFILENAME)

        ctx = sm.ServiceContext(OUTFILENAME)
        svc = filter(lambda x: x.name == "collectorredis", ctx.services)[0]
        monpro = svc.monitoringProfile
        self.assertEqual(len(monpro.graphConfigs), 1)
        gc_ids = [gc.graphID for gc in monpro.graphConfigs]
        self.assertEqual(len(gc_ids), 1)
        self.assertTrue('metricqueue' not in gc_ids)

    def test_graphconfig_add(self):
        """
        Tests creating and adding a new GraphConfig to a MonitoringProfile.
        """
        ctx = sm.ServiceContext(INFILENAME)
        svc = filter(lambda x: x.name == "HMaster", ctx.services)[0]
        monpro = svc.monitoringProfile
        self.assertEqual(len(monpro.graphConfigs), 0)
        gc = sm.monitoringprofile.graphconfig.GraphConfig(
            graphID="widgets")
        gc.datapoints = [sm.graphdatapoint.GraphDatapoint(pointType="dot")]
        monpro.graphConfigs.append(gc)
        ctx.commit(OUTFILENAME)
        ctx = sm.ServiceContext(OUTFILENAME)
        svc = filter(lambda x: x.name == "HMaster", ctx.services)[0]
        monpro = svc.monitoringProfile
        self.assertEqual(len(monpro.graphConfigs), 1)
        gc_ids = [gc.graphID for gc in monpro.graphConfigs]
        self.assertEqual(len(gc_ids), 1)
        self.assertTrue('widgets' in gc_ids)
        self.assertEqual(len(monpro.graphConfigs[0].datapoints), 1)
        self.assertEqual(monpro.graphConfigs[0].datapoints[0].pointType, "dot")

    def test_graphconfig_modify(self):
        """
        Tests modifying a GraphConfig of a MonitoringProfile in place.
        """
        ctx = sm.ServiceContext(INFILENAME)
        svc = filter(lambda x: x.name == "CentralQuery", ctx.services)[0]
        monpro = svc.monitoringProfile
        self.assertEqual(len(monpro.graphConfigs), 1)
        monpro.graphConfigs[0].description = "Modified description"
        monpro.graphConfigs[0].datapoints[0].pointType = "dot"
        ctx.commit(OUTFILENAME)
        ctx = sm.ServiceContext(OUTFILENAME)
        svc = filter(lambda x: x.name == "CentralQuery", ctx.services)[0]
        monpro = svc.monitoringProfile
        self.assertEqual(len(monpro.graphConfigs), 1)
        desc = monpro.graphConfigs[0].description
        self.assertEqual(desc, "Modified description")
        pt = monpro.graphConfigs[0].datapoints[0].pointType
        self.assertEqual(pt, "dot")

    def test_tags_filter(self):
        """
        Tests filtering a service by tags.
        """
        ctx = sm.ServiceContext(INFILENAME)
        svcs = filter(lambda s: "collector" in s.tags and "daemon" in s.tags, ctx.services)
        self.assertEqual(len(svcs), 14)

    def test_tags_alter(self):
        """
        Tests altering the tag list of a service.
        """
        ctx = sm.ServiceContext(INFILENAME)
        svc = filter(lambda s: "collector" in s.tags and "daemon" in s.tags, ctx.services)[0]
        svc.tags.remove("collector")
        svc.tags.append("unlikely_tag")
        ctx.commit(OUTFILENAME)
        ctx = sm.ServiceContext(OUTFILENAME)
        svcs = filter(lambda s: "unlikely_tag" in s.tags and "daemon" in s.tags, ctx.services)
        self.assertEqual(len(svcs), 1)

    def test_tags_replace(self):
        """
        Tests completely replacing the tag list of a service.
        """
        ctx = sm.ServiceContext(INFILENAME)
        svc = filter(lambda s: "collector" in s.tags and "daemon" in s.tags, ctx.services)[0]
        svc.tags = ["unlikely_tag_1", "unlikely_tag_2"]
        ctx.commit(OUTFILENAME)
        ctx = sm.ServiceContext(OUTFILENAME)
        svcs = filter(lambda s: "unlikely_tag_1" in s.tags and "unlikely_tag_2" in s.tags, ctx.services)
        self.assertEqual(len(svcs), 1)

    def tests_logconfigs_add(self):
        """
        Tests adding a new file to a service's LogConfigs.
        """
        ctx = sm.ServiceContext(INFILENAME)
        svc = filter(lambda x: x.description == "Zope server", ctx.services)[0]
        self.assertEqual(len(svc.logConfigs), 3)
        svc.logConfigs.append(sm.LogConfig(path="/opt/zenoss/log/honk.log",
                                           logType="honk"))
        ctx.commit(OUTFILENAME)
        ctx = sm.ServiceContext(OUTFILENAME)
        svc = filter(lambda x: x.description == "Zope server", ctx.services)[0]

        if not "honk" in [hc.logType for hc in svc.logConfigs]:
            raise ValueError("Failed to alter logconfigs.")
        for lc in svc.logConfigs:
            if lc.logType == "honk":
                self.assertEqual(lc.path, "/opt/zenoss/log/honk.log")
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

    def test_clone_service(self):
        """
        Tests cloning a service.
        """
        ctx = sm.ServiceContext(INFILENAME)
        self.assertEqual(len(ctx.services), 34)
        redis = filter(lambda s: s.name == "redis", ctx.services)[0]
        clone = redis.clone()
        clone.name = "clone name"
        ctx.services.append(clone)
        ctx.commit(OUTFILENAME)
        ctx = sm.ServiceContext(OUTFILENAME)
        clone = filter(lambda s: s.name == "clone name", ctx.services)[0]
        self.assertEqual(clone.description, redis.description)
        self.assertEqual(len(ctx.services), 35)

