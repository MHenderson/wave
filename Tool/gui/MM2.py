import dbif

def dr(contains, requires, supplies):
    return dbif.diff(dbif.diff(dbif.join(contains, requires), dbif.join(contains, supplies)), requires)
