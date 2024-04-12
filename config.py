from urllib.parse import urlparse

ENV = "dev"

if ENV == 'dev':
    DATABASE_CONFIG = {
        'host': "localhost",
        'database': "dieDB",
        'user': "jacklofwall",
        'password': ""
    }
else: 
    uri = "*****"
    parsed_uri = urlparse(uri)

    DATABASE_CONFIG = {
        'host': "*****",
        'database': "****",
        'user': "****",
        'password': "****",
        'port': "5432"
    } 
