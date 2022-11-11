import psycopg2

db_name = "stocks"
db_host = "localhost"
db_user = "watch"
db_pass = "watch"
db_port = 5432

# https://medium.com/the-handbook-of-coding-in-finance/building-financial-data-storage-with-postgresql-in-python-b981e38826fe
# some simple example of how to connect and write data tables

def connect():
    conn = psycopg2.connect(database=db_name,
                            host=db_host,
                            user=db_user,
                            password=db_pass,
                            port=db_port)
    conn.autocommit = True
    return conn

def create_database(database):
    conn = psycopg2.connect(database=db_name,
                            host=db_host,
                            user=db_user,
                            password=db_pass,
                            port=db_port)
    conn.autocommit = True
    cursor = conn.cursor()
    sql = '''CREATE DATABASE ''' + database;
    cursor.execute(sql)
    print("Database created successfully!")
    conn.close()

def create_table(table, db_name):
    conn = psycopg2.connect(database=db_name,
                            host=db_host,
                            user=db_user,
                            password=db_pass,
                            port=db_port)
    conn.autocommit = True
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE prices
                (
                    Date DATE NOT NULL,
                    Open FLOAT NOT NULL,
                    High FLOAT NOT NULL,
                    Low FLOAT NOT NULL,
                    Close FLOAT NOT NULL,
                    Adj_Close FLOAT NOT NULL,
                    Volume BIGINT NOT NULL,
                    Ticker VARCHAR(255) NOT NULL
                    );''')
                
    print("Table created successfully")
    conn.close()

print("success!")