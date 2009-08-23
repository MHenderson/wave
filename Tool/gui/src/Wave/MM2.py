import dbif
from dbif import join, diff, dr, dom

def DR(contains, requires, supplies):
    return diff(diff(join(contains, requires), join(contains, supplies)), requires)

def DS(contains, supplies):
    return diff(dr(dom(contains), supplies), join(contains, supplies))

