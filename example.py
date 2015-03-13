import servicemigration as sm
sm.require("1.0.0")

# Get the service context.
ctx = sm.ServiceContext()

# Get the first zope service we come across.
zope = filter(lambda x: x.description == "Zope server", ctx.services)[0]

# Change the description.
zope.description = "unlikelY"

# Change the startup command.
zope.startup = "unlikelY"

# Remove the zenhub and mariadb endpoints.
zope.endpoints = filter(lambda ep: ep.name not in ["zenhub", "mariadb"], zope.endpoints)

# Get the redis endpoint.
redis = filter(lambda ep: ep.name == "redis", zope.endpoints)[0]

# Alter the name, protocol, and addressConfig port of the redis endpoint.
redis.name = "unlikelY"
redis.protocol = "unlikelY"
redis.addressConfig.port = 1337

# Add a new endpoint.
zope.endpoints.append(sm.Endpoint(
    name = "unlikelY-2",
    purpose = "unlikelY",
    application = "unlikelY",
    portnumber = 1337,
    protocol = "unlikelY",
    addressConfig = sm.AddressConfig(1337, "unlikelY")
))

# Remove the help and upgrade runs.
zope.runs = filter(lambda r: r.name not in ["help", "upgrade"], zope.runs)

# Get the zendmd run.
zendmd = filter(lambda r: r.name == "zendmd", zope.runs)[0]

# Alter the zendmd name and command.
zendmd.name = "unlikelY"
zendmd.command = "unlikelY"

# Add a new run.
zope.runs.append(sm.Run("unlikelY-2", "unlikelY"))

# Remove the zenjobs volume.
zope.volumes = filter(lambda v: v.resourcePath != "zenjobs", zope.volumes)

# Get the .ssh volume.
ssh = filter(lambda v: v.resourcePath == ".ssh", zope.volumes)[0]

# Alter the owner and permission of the ssh volume.
ssh.owner = "unlikelY"
ssh.permission = "unlikelY"

# Add a new volume.
zope.volumes.append(sm.Volume("unlikelY","unlikelY","unlikelY","unlikelY"))

# Remove the running and answering healthchecks.
zope.healthChecks = filter(lambda hc: hc.name not in ["running", "answering"], zope.healthChecks)

# Get the rabbit_answering health check.
rabbit = filter(lambda hc: hc.name == "rabbit_answering", zope.healthChecks)[0]

# Alter the rabbit_answering health check.
rabbit.name = "unlikelY"
rabbit.interval = 9001

# Add a new health check
zope.healthChecks.append(sm.HealthCheck("unlikelY","unlikelY",10, 1000))

# Set the version of all services.
ctx.version = "unlikelY"

# Commit the changes. Done!
ctx.commit()


