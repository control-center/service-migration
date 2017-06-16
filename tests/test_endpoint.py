import unittest
import os

import servicemigration as sm
sm.require(sm.version.API_VERSION)

INFILENAME = os.path.join(os.path.dirname(__file__), "v1.0.0.json")
OUTFILENAME = os.path.join(os.path.dirname(__file__), "out.json")

class ServiceTest(unittest.TestCase):

    def test_portTemplate_change(self):
        """
        Tests changing an imageID
        """

        new_template = "{ plus 9000 .InstanceID }"
        ctx = sm.ServiceContext(INFILENAME)
        svc = filter(lambda x: x.description == "Region Server for HBase", ctx.services)[0]
        regionserver_ep = filter(lambda ep: ep.name == 'hbase-regionserver', svc.endpoints)[0]
        regionserver_ep.porttemplate = new_template
        ctx.commit(OUTFILENAME)
        ctx = sm.ServiceContext(OUTFILENAME)
        svc = filter(lambda x: x.description == "Region Server for HBase", ctx.services)[0]
        regionserver_ep = filter(lambda ep: ep.name == 'hbase-regionserver', svc.endpoints)[0]
        self.assertEqual(regionserver_ep.porttemplate, new_template)
