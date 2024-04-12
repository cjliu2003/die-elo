import psycopg2 
import config

# Connect to the database
conn = psycopg2.connect(
    host=config.DATABASE_CONFIG['host'],
    database=config.DATABASE_CONFIG['database'],
    user=config.DATABASE_CONFIG['user'],
    password=config.DATABASE_CONFIG['password']
)

# Print a message if the connection is successful
print("Connected to the database!")

# Close the connection
conn.close()
