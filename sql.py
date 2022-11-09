import psycopg2

db_name = "ai"
db_host = "localhost"
db_user = "watch"
db_pass = "watch"
db_port = 5432

conn = psycopg2.connect(database=db_name,
                        host=db_host,
                        user=db_user,
                        password=db_pass,
                        port=db_port)

cursor = conn.cursor()

print("success!")