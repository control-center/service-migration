import servicemigration as sm
sm.require("1.0.0")

ctx = sm.ServiceContext()

zope = filter(lambda x: x.description == "Zope server", ctx.services)[0]
zope.description = "unlikelY"
zope.startup = "unlikelY"
zope.endpoints[0].name = "unlikelY"
zope.endpoints[0].addressConfig.protocol = "unlikelY"
zope.runs[0].name = "unlikelY"
zope.runs[0].command = "unlikelY"
zope.volumes[0].owner = "unlikelY"
zope.healthChecks[0].script = "unlikelY"

ctx.version = "unlikelY"

ctx.commit()


