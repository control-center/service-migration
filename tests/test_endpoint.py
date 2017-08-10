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

    def test_add_vhost(self):
        ctx = sm.ServiceContext(INFILENAME)
        svc = filter(lambda x: x.name == 'Zenoss.core', ctx.services)[0]
        zproxy_ep = filter(lambda ep: ep.name == 'zproxy', svc.endpoints)[0]
        vhostlist_len = len(zproxy_ep.vhostlist)
        zproxy_ep.vhostlist.append(sm.VHost(name="zendebug", enabled=True))
        ctx.commit(OUTFILENAME)
        ctx = sm.ServiceContext(OUTFILENAME)
        svc = filter(lambda x: x.name == 'Zenoss.core', ctx.services)[0]
        zproxy_ep = filter(lambda ep: ep.name == 'zproxy', svc.endpoints)[0]
        self.assertEqual(vhostlist_len+1, len(zproxy_ep.vhostlist) )
        vhost = filter(lambda v: v.name == 'zendebug', zproxy_ep.vhostlist)[0]
        self.assertEqual(vhost.name, "zendebug")
        self.assertEqual(vhost.enabled, True)


    def test_add_port(self):
        ctx = sm.ServiceContext(INFILENAME)
        svc = filter(lambda x: x.name == 'Zenoss.core', ctx.services)[0]
        zproxy_ep = filter(lambda ep: ep.name == 'zproxy', svc.endpoints)[0]
        portlist_len = len(zproxy_ep.portlist)
        zproxy_ep.portlist.append(sm.Port(portaddr="acme99.example.com:8849", protocol="https", enabled=True, usetls=True))
        ctx.commit(OUTFILENAME)
        ctx = sm.ServiceContext(OUTFILENAME)
        svc = filter(lambda x: x.name == 'Zenoss.core', ctx.services)[0]
        zproxy_ep = filter(lambda ep: ep.name == 'zproxy', svc.endpoints)[0]
        self.assertEqual(portlist_len+1, len(zproxy_ep.portlist) )
        port = filter(lambda p: p.portaddr == "acme99.example.com:8849", zproxy_ep.portlist)[0]
        self.assertEqual(port.portaddr, "acme99.example.com:8849")
        self.assertEqual(port.protocol, "https")
        self.assertEqual(port.enabled, True)
        self.assertEqual(port.usetls, True)
