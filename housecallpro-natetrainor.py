# Necessary imports
import json
import unicodedata

# Test script
# print ("Hello World")

# Create visit object
class Visit(object):
    full_visitor_id = ""
    visit_id = ""
    visit_number = 0
    visit_start_time = ""
    browser = ""
    country = ""

    # The class "constructor" - It's actually an initializer 
    def __init__(self, full_visitor_id, visit_id, visit_number, visit_start_time, browser, country):
        self.full_visitor_id = full_visitor_id
        self.visit_id = visit_id
        self.visit_number = visit_number
        self.visit_start_time = visit_start_time
        self.browser = browser
        self.country = country

def make_visit(full_visitor_id, visit_id, visit_number, visit_start_time, browser, country):
    visit = Visit(full_visitor_id, visit_id, visit_number, visit_start_time, browser, country)
    return visit

# Create hit object
class Hit(object):
    hit_visitor = ""
    hit_number = 0
    hit_type = ""
    hit_timestamp = ""
    page_path = ""
    page_title = ""
    hostname = ""

    # The class "constructor" - It's actually an initializer 
    def __init__(self, hit_visitor, hit_number, hit_type, hit_timestamp, page_path, page_title, hostname):
        self.hit_visitor = hit_visitor
        self.hit_number = hit_number
        self.hit_type = hit_type
        self.hit_timestamp = hit_timestamp
        self.page_path = page_path
        self.page_title = page_title
        self.hostname = hostname

def make_hit(hit_visitor, hit_number, hit_type, hit_timestamp, page_path, page_title, hostname):
    hit = Hit(hit_visitor, hit_number, hit_type, hit_timestamp, page_path, page_title, hostname)
    return hit

# Set up VisitEncoder
class VisitEncoder(json.JSONEncoder):
    def default(self, o): 
        if isinstance(o, Visit):
           # JSON object would be a dictionary.
            return {
                "full_visitor_id" : o.full_visitor_id,
                "visit_id": o.visit_id,
                "visit_number" : o.visit_number,
                "visit_start_time" : o.visit_start_time,
                "browser" : o.browser,
                "country": o.country
            } 
        else:
            # Base class will raise the TypeError.
            return super().default(o)

# Set up HitEncoder
class HitEncoder(json.JSONEncoder):
    def default(self, o): 
        if isinstance(o, Hit):
           # JSON object would be a dictionary.
            return {
                "hit_visitor" : o.hit_visitor,
                "hit_number": o.hit_number,
                "hit_type" : o.hit_type,
                "hit_timestamp" : o.hit_timestamp,
                "page_path" : o.page_path,
                "page_title" : o.page_title,
                "hostname": o.hostname
            } 
        else:
            # Base class will raise the TypeError.
            return super().default(o)

# Read input file
session_data = open('ga_sessions_20160801.json', 'r')
session_lines = session_data.readlines()

visits=[]
hits=[]

for line in session_lines:
    session = json.loads(line)

    device = session['device']
    geoNetwork = session['geoNetwork']

    fullVisitorId = str(session['fullVisitorId'])
    visitId = str(session['visitId'])
    visitNumber = int(session['visitNumber'])
    visitStartTime = str(session['visitStartTime'])
    browser = str(device['browser'])
    country = str(geoNetwork['country'])

    visit = make_visit(fullVisitorId, visitId, visitNumber, visitStartTime, browser, country)

    print
    print ("*****")
    print (vars(visit))
    print ("*****")
    print

    visits.append(visit)

    for initial_hit in session['hits']:
        page = initial_hit['page']

        hitNumber = int(initial_hit['hitNumber'])
        type = str(initial_hit['type'])
        # Unicode normalization may be needed for other string components
        # Just added for pageTitle and pagePath only as it is the only variable that could conceivably need it
        pagePath = unicodedata.normalize('NFKD', page['pagePath']).encode('ascii', 'ignore')
        pageTitle = unicodedata.normalize('NFKD', page['pageTitle']).encode('ascii', 'ignore')
        hostname = str(page['hostname'])

        time = int(initial_hit['time'])
        hitTime = int(visitStartTime) + time
        hitTimestamp = str(hitTime)

        hit = make_hit(fullVisitorId, hitNumber, type, hitTimestamp, pagePath, pageTitle, hostname)

        print
        print ("-----")
        print (vars(hit))
        print ("-----")
        print

        hits.append(hit)

print
print (len(visits))
print (len(hits))
print

# Generate visits.json
with open('visits.json', 'w') as f:
    json.dump(visits, f, cls=VisitEncoder, indent=2)

# Generate hits.json
with open('hits.json', 'w') as f:
    json.dump(hits, f, cls=HitEncoder, indent=2)

# Tried experimenting with the json.dump command in the hopes of getting each item on its own line, but without success