import psycopg2

hostname = 'localhost'
dbport = '5432'
dbname = 'postgres_db'
dbuser = 'postgres'
dbpass = '****'
table_name = 'default_table'

conn = psycopg2.connect(database=dbname, user = dbuser, password = dbpass, host = hostname, port = dbport)
print("Connected to DB")
conn.autocommit = True

cur = conn.cursor()

cur.execute('''CREATE TABLE ${table_name}(
            SNO INT NOTNULL,
            DATE DATE NOTNULL,
            DATA VARCHAR(20) NOTNULL
            ); ''')