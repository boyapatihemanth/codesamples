import psycopg2

hostname = 'localhost'
dbport = '5432'
dbname = 'postgres_db'
dbuser = 'postgres'
dbpass = '****'
table_name = 'default_table'
csv_file_name = 'data.csv'

def commit_csv_to_postgresql(hostname, dbport, dbname, dbuser, dbpass, table_name, csv_file_name):
    conn = psycopg2.connect(database=dbname, user = dbuser, password = dbpass, host = hostname, port = dbport)
    cur = conn.cursor()
    with open(csv_file_name, 'r') as f:
        next(f)
        cur.copy_from(f, table_name, sep = ',')
        conn.commit()


if __name__ == '__main__':
    commit_csv_to_postgresql(hostname, dbport, dbname, dbuser, dbpass, table_name, csv_file_name)