import psycopg2

db_name = "quotes"
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
    print("Connect Success! Host:" + db_host + " Database:" + db_name)
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

    cursor.execute('''CREATE TABLE ''' + table + ''' 
                (
                    ticker VARCHAR(255) NOT NULL
                    date DATE NOT NULL,
                    time TIME NOT NULL,
                    name VARCHAR(255) NOT NULL
                    price FLOAT NOT NULL,
                    close FLOAT NOT NULL,
                    open FLOAT NOT NULL,
                    bid FLOAT NOT NULL,
                    bidSize BIGINT NOT NULL,
                    ask FLOAT NOT NULL,
                    askSize BIGINT NOT NULL,
                    high FLOAT NOT NULL,
                    low FLOAT NOT NULL,
                    52high FLOAT NOT NULL,
                    52low FLOAT NOT NULL,
                    volume BIGINT NOT NULL,
                    avgVolume BIGINT NOT NULL,
                    marketCap BIGINT NOT NULL,
                    beta FLOAT NOT NULL,
                    pe FLOAT NOT NULL,
                    eps FLOAT NOT NULL,
                    earningsDate DATE NOT NULL,
                    dividend FLOAT NOT NULL,
                    yield FLOAT NOT NULL,
                    exdivDate DATE NOT NULL,
                    target FLOAT NOT NULL
                    );''')
                
    print("Table created successfully")
    conn.close()