import servicemigration as sm
sm.require("1.0.0")

ctx = sm.ServiceContext()

def myFilter(item):
    return item.getDescription() == "Zope server"

for service in filter(myFilter, ctx.services):
    service.setDescription("an_unlikely-description")
    runs = service.getRuns()
    runs["foo"] = "an_unlikely-run"
    service.setRuns(runs)

ctx.commit()


