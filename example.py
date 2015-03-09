import servicemigration as sm
sm.require("1.0.0")

ctx = sm.ServiceContext()

def myFilter(item):
    return item.description == "Zope server"

for service in filter(myFilter, ctx.services):
    service.description = "an_unlikely-description"
    service.runs["foo"] = "bar"

ctx.commit()


