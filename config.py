from urllib.parse import urlparse

ENV = "prod"

if ENV == 'dev':
    DATABASE_CONFIG = {
        'host': "localhost",
        'database': "dieDB",
        'user': "jacklofwall",
        'password': ""
    }
else: 
    #uri = "postgresql://jlofwall:Q4#ruxug@toss-db-id.c9oc0e2aqo0j.us-east-2.rds.amazonaws.com:5432/dieDB"
    #parsed_uri = urlparse(uri)
    #print(parsed_uri)
    DATABASE_CONFIG = {
        'host': "toss-db-id.c9oc0e2aqo0j.us-east-2.rds.amazonaws.com",
        'database': "dieDB",
        'user': "jlofwall",
        'password': "Q4#ruxug",
        'port': "5432"
    } 
