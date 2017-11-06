import sys
import pymysql

rds_host  = ""
name = ""
password = ""
db_name = ""
port = 3306

def connect():
    try:
        conn = pymysql.connect(rds_host, user=name,
                               passwd=password, db=db_name, connect_timeout=5)
        print("SUCCESS: Connection to RDS mysql instance succeeded")
        return conn
    except:
        print("ERROR: Unexpected error: Could not connect to MySql instance.")
        sys.exit()


if __name__ == '__main__':
    conn = connect()
    item_count = 0
    with conn.cursor() as cur:
        cur.execute("create table Test1 (id int NOT NULL, name varchar(255) NOT NULL, PRIMARY KEY (id))")
        for i in xrange(0, 100):
            cur.execute('insert into Test1 (id, name) values({i}, "name_{i}")'.format(i=i))
            conn.commit()
        cur.execute("select * from Test1")
        for row in cur:
            item_count += 1
            print(row)
    print("Added {} items to RDS MySQL table".format(item_count))
    conn.close()