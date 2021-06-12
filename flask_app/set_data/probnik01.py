import sys, json, os
from psycopg2 import connect, Error




def get_data():
    try:
        conn = connect(
            dbname="campers4",
            user="postgres",
            host="localhost",
            password="oSaka_2019",
            # attempt to connect for 3 seconds then raise exception
            connect_timeout=3)

        cur = conn.cursor()
        print("\ncreated cursor object:", cur)

        sql = 'SELECT name FROM models;'




        cur.execute(sql)
        a = cur.fetchall()

        for i in a:
            if i is not None:
                for d in i:
                    print(d)


        cur.close()
        conn.close()
    except Error as err:
        print(err)


if __name__ == '__main__':
    get_data()
