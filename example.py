import servicemigration as sm
sm.require("1.0.0")

"""
This example script should make the following changes:

        - The version of every service is changed to 1234567890

        - The description of all the children of the service named/described 
          "localhost"/"Localhost collector" are changed to "child description".    

        - The description of the service named "Zenoss.core" is changed to "parent description".

        - The service named "redis" is cloned and altered:

                - Name is changed to "clone name"

                - The exported endpoint Application property is changed to "endpoint_application"

                - The DesiredState is set to RUN (1)

        - The service named "Zope" and having the description "Zope server" is altered:

                - Name is changed to "service name"

                - Description is changed to "service description"

                - Startup is changed to "service startup"

                - Endpoint "zenhub" is removed

                - Endpoint "mariadb" is altered:
                    - Name is changed to "altered mariadb"
                    - Purpose is changed to "export"
                    - Application is changed to "application"
                    - Portnumber is changed to 1234
                    - Protocol is changed to "TCP"
                    - AddressConfig is altered:
                        - Port is changed to 5678
                        - Protocol is changed to "UDP"

                - A new endpoint is added:
                    - Name: "endpoint name"
                    - Purpose: "import"
                    - Application: "application"
                    - Portnumber: 9012
                    - Protocol: "TCP"
                    - AddressConfig:
                        - Port: 3456
                        - Protocol: "UDP"

                - Run "help" is removed

                - Run "upgrade" is altered:
                    - Name is changed to "upgrade renamed"
                    - Command is changed to "upgrade command"

                - A new Run is added:
                    - Name: "new run"
                    - Command: "new run command"

                - Volume having the resource path "zenjobs" is removed

                - Volume having the resource path ".ssh" is altered:
                    - Owner is changed to "ssh owner"
                    - Permission is changed to "0000"
                    - Resource path is changed to "ssh resource path"
                    - Container path is changed to "/new/volume/container/path"

                - HealthCheck "answering" is removed

                - HealthCheck "running" is altered:
                    - Name is changed to "running name"
                    - Script is changed to "running script"
                    - Interval is changed to 123
                    - Timeout is changed to 456

                - A new HealthCheck is added:
                    - Name: "new healthcheck name"
                    - Script: "new healthcheck script"
                    - Interval: 789
                    - Timeout: 901

                - ConfigFile "/opt/zenoss/etc/global.conf" is removed

                - ConfigFile "/opt/zenoss/etc/zope.conf" is altered:
                    - Name: "Zope config name"
                    - Filename: "zope_config_filename"
                    - Owner: "foo:bar"
                    - Permissions: 777
                    - Content: "Zope conf contents"

                - A new ConfigFile is added:
                    - Name: "new configfile name"
                    - Filename: "new configfile filename"
                    - Owner: "new configfile owner"
                    - Permissions: 111
                    - Content: "new configfile content"

                - InstanceLimits is altered:
                    - Min is changed to 0
                    - Max is changed to 2
                    - Default is changed to 2
"""

# Get the service context.
ctx = sm.ServiceContext()

# Get the first zope service we come across.
svc = filter(lambda x: x.name == "Zope" and x.description == "Zope server", ctx.services)[0]

# Change the name.
svc.name = "service name"

# Change the description.
svc.description = "service description"

# Change the startup
svc.startup = "service startup"

# Remove the zenhub endpoint.
svc.endpoints = filter(lambda x: x.name != "zenhub", svc.endpoints)

# Alter the mariadb endpoint.
maria = filter(lambda x: x.name == "mariadb", svc.endpoints)[0]
maria.name = "altered mariadb"
maria.purpose = "export"
maria.application = "application"
maria.portnumber = 1234
maria.protocol = "TCP"
maria.addressConfig = sm.AddressConfig(5678, "UDP")

# Add a new endpoint
svc.endpoints.append(sm.Endpoint(
    name = "endpoint name",
    purpose = "import",
    application = "application",
    portnumber = 9012,
    protocol = "TCP",
    addressConfig = sm.AddressConfig(3456, "UDP")
))

# Remove the "help" run.
svc.runs = filter(lambda x: x.name != "help", svc.runs)

# Alter the "upgrade" run.
upgrade = filter(lambda x: x.name == "upgrade", svc.runs)[0]
upgrade.name = "upgrade renamed"
upgrade.command = "upgrade command"

# Add a new run.
svc.runs.append(sm.Run("new run", "new run command"))

# Remove the "zenjobs" volume.
svc.volumes = filter(lambda x: x.resourcePath != "zenjobs", svc.volumes)

# Alter the ".ssh" volume.
ssh = filter(lambda x: x.resourcePath == ".ssh", svc.volumes)[0]
ssh.owner = "ssh owner"
ssh.permission = "0000"
ssh.resourcePath = "ssh resource path"
ssh.containerPath = "ssh/container/path"

# Create a new volume.
svc.volumes.append(sm.Volume(
    owner = "new volume owner",
    permission = "1111",
    resourcePath = "new volume resource path",
    containerPath = "new/volume/container/path"
))

# Remove the "answering" health check.
svc.healthChecks = filter(lambda x: x.name != "answering", svc.healthChecks)

# Alter the "running" health check.
running = filter(lambda x: x.name == "running", svc.healthChecks)[0]
running.name = "running name"
running.script = "running script"
running.interval = 123
running.timeout = 456

# Add a new health check.
svc.healthChecks.append(sm.HealthCheck(
    name = "new healthcheck name",
    script = "new healthcheck script",
    interval = 789,
    timeout = 901
))

# Remove the "/opt/zenoss/etc/global.conf" config file.
svc.configFiles = filter(lambda x: x.name != "/opt/zenoss/etc/global.conf", svc.configFiles)

# Alter the "/opt/zenoss/etc/zope.conf" config file.
zopeconf = filter(lambda x: x.name == "/opt/zenoss/etc/zope.conf", svc.configFiles)[0]
zopeconf.name = "Zope config name"
zopeconf.filename = "zope_config_filename"
zopeconf.owner = "foo:bar"
zopeconf.permissions = 777
zopeconf.content = "Zope conf contents"

# Add a new config file.
svc.configFiles.append(sm.ConfigFile(
    name = "new configfile name",
    filename = "new configfile filename",
    owner = "new configfile owner",
    permissions = 111,
    content = "new configfile content"
))

# Alter the instance limits.
svc.instanceLimits.minimum = 0
svc.instanceLimits.maximum = 2
svc.instanceLimits.default = 2

# Alter the version of all services.
ctx.version = "1234567890"

# Change the description of all the children of the service named/described
# "localhost"/"Localhost collector" to "child description".
parent = filter(lambda x: x.name == "localhost" and x.description == "Localhost collector", ctx.services)[0]
for child in ctx.getServiceChildren(parent):
    child.description = "child description"

# Find the "collectorredis" service and follow the tree up to "Zenoss.core". Change the description
# of "Zenoss.core" to "parent description".
child = filter(lambda x: x.name == "collectorredis", ctx.services)[0]
while ctx.getServiceParent(child):
    child = ctx.getServiceParent(child)
child.description = "parent description"

# Make a clone of the redis service.
redis = filter(lambda x: x.name == "redis", ctx.services)[0]
newRedis = ctx.cloneService(redis)

# Rename it to "clone name"
newRedis.name = "clone name"

# Rename the exported endpoint application to "endpoint_application"
export = filter(lambda e: e.purpose == "export", newRedis.endpoints)[0]
export.application = "endpoint_application"

# Set the desired state to RUN.
newRedis.desiredState = sm.RUN

# Commit the changes.
ctx.commit()
