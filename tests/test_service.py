import unittest
import os

import servicemigration as sm
sm.require(sm.version.API_VERSION)

INFILENAME = os.path.join(os.path.dirname(__file__), "v1.0.0.json")
OUTFILENAME = os.path.join(os.path.dirname(__file__), "out.json")

class ServiceTest(unittest.TestCase):

    def test_get_services(self):
        """
        Tests ServiceContext creation.
        """
        ctx = sm.ServiceContext(INFILENAME)

    def test_description_add(self):
        """
        Tests adding a description where one did not previously exist.
        """
        ctx = sm.ServiceContext(INFILENAME)
        svc = filter(lambda x: x.getDescription() == "Zope server", ctx.services)[0]
        del svc._Service__data["Description"]
        svc.setDescription("an_unlikely-description")
        ctx.commit(OUTFILENAME)
        ctx = sm.ServiceContext(OUTFILENAME)
        svc = filter(lambda x: x.getDescription() == "an_unlikely-description", ctx.services)
        self.assertEqual(len(svc), 1)

    def test_description_remove(self):
        """
        Tests completely removing a description.
        """
        ctx = sm.ServiceContext(INFILENAME)
        svc = filter(lambda x: x.getDescription() == "Zope server", ctx.services)[0]
        svc.setDescription(None)
        ctx.commit(OUTFILENAME)
        ctx = sm.ServiceContext(OUTFILENAME)
        svc = filter(lambda x: x.getDescription() == None, ctx.services)
        self.assertEqual(len(svc), 1)

    def test_description_change(self):
        """
        Tests altering a description.
        """
        ctx = sm.ServiceContext(INFILENAME)
        svc = filter(lambda x: x.getDescription() == "Zope server", ctx.services)[0]
        svc.setDescription("an_unlikely-description")
        ctx.commit(OUTFILENAME)
        ctx = sm.ServiceContext(OUTFILENAME)
        svc = filter(lambda x: x.getDescription() == "an_unlikely-description", ctx.services)
        self.assertEqual(len(svc), 1)

    def test_runs_add_prev_none(self):
        """
        Tests adding a run where there were previously none.
        """
        ctx = sm.ServiceContext(INFILENAME)
        svc = filter(lambda x: x.getDescription() == "Zope server", ctx.services)[0]
        del svc._Service__data["Runs"]
        runs = svc.getRuns()
        runs["foo"] = "an_unlikely-run"
        svc.setRuns(runs)
        ctx.commit(OUTFILENAME)
        ctx = sm.ServiceContext(OUTFILENAME)
        svc = filter(lambda x: x.getDescription() == "Zope server", ctx.services)[0]
        runs = svc.getRuns()
        self.assertEqual(runs["foo"], "an_unlikely-run")

    def test_runs_remove(self):
        """
        Tests removing specific runs.
        """
        ctx = sm.ServiceContext(INFILENAME)
        svc = filter(lambda x: x.getDescription() == "Zope server", ctx.services)[0]
        runs = svc.getRuns()
        del runs["apply-custom-patches"]
        del runs["help"]
        svc.setRuns(runs)
        ctx.commit(OUTFILENAME)
        ctx = sm.ServiceContext(OUTFILENAME)
        svc = filter(lambda x: x.getDescription() == "Zope server", ctx.services)[0]
        runs = svc.getRuns()
        self.assertEqual(len(runs), 5)
        if "help" in runs:
            raise ValueError("Error removing run.")
        if "apply-custom-patches" in runs:
            raise ValueError("Error removing run.")

    def test_runs_add(self):
        """
        Tests adding runs to an existing list.
        """
        ctx = sm.ServiceContext(INFILENAME)
        svc = filter(lambda x: x.getDescription() == "Zope server", ctx.services)[0]
        runs = svc.getRuns()
        runs["foo"] = "an_unlikely-run"
        runs["bar"] = "an_unlikely-run"
        runs["baz"] = "an_unlikely-run"
        svc.setRuns(runs)
        ctx.commit(OUTFILENAME)
        ctx = sm.ServiceContext(OUTFILENAME)
        svc = filter(lambda x: x.getDescription() == "Zope server", ctx.services)[0]
        runs = svc.getRuns()
        self.assertEqual(runs["foo"], "an_unlikely-run")
        self.assertEqual(runs["bar"], "an_unlikely-run")
        self.assertEqual(runs["baz"], "an_unlikely-run")
        self.assertEqual(len(runs), 10)

    def test_runs_replace(self):
        """
        Tests completely replacing the runs map.
        """
        ctx = sm.ServiceContext(INFILENAME)
        svc = filter(lambda x: x.getDescription() == "Zope server", ctx.services)[0]
        runs = {
            "foo": "bar",
            "bar": "baz",
            "baz": "foo"
        }
        svc.setRuns(runs)
        ctx.commit(OUTFILENAME)
        ctx = sm.ServiceContext(OUTFILENAME)
        svc = filter(lambda x: x.getDescription() == "Zope server", ctx.services)[0]
        self.assertEqual(runs["foo"], "bar")
        self.assertEqual(runs["bar"], "baz")
        self.assertEqual(runs["baz"], "foo")
        self.assertEqual(len(runs), 3)
