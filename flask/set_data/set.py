import sys, json, os
from psycopg2 import connect, Error


def get_data():
    try:
        conn = connect(
            port = 5434,
            dbname="campers4",
            user="postgres",
            host="localhost",
            password="postgres",
            # attempt to connect for 3 seconds then raise exception
            connect_timeout=3)

        cur = conn.cursor()
        print("\ncreated cursor object:", cur)

        sql = """SELECT table_name
               FROM information_schema.tables
               WHERE table_schema='public'
               AND table_type='BASE TABLE';
              """

        cur.execute(sql)
        list_all_tables = cur.fetchall()
        cur.close()
        cur = conn.cursor()

        data = {}

        k = 0
        for i in range(len(list_all_tables)):
            k+=1
            table = list_all_tables[i][0]


            sql2 = '''select column_name from information_schema.columns where table_name = '{}';'''.format(table)
            cur.execute(sql2)
            list_all_columns_in_table = cur.fetchall()

            sql3 = 'SELECT count(*) FROM {};'.format(table)
            cur.execute(sql3)
            count_row = cur.fetchall()
            count_row = int(count_row[0][0])
            w = 1
            rows = []
            while count_row > 0:

                data_fields = {}
                for j in range(len(list_all_columns_in_table)):

                    field = list_all_columns_in_table[j][0]

                    sql4 ='SELECT {} FROM {} WHERE id={};'.format(field, table, w)
                    cur.execute(sql4)
                    c = cur.fetchone()

                    data_fields[field] = c[0]
                rows.append(data_fields)

                count_row = count_row - 1
                w+=1

            data[table] = rows

        cur.close()
        conn.close()


        person_json = json.dumps(data)

        with open('postgres-records2.json', 'w') as js_ms:
               js_ms.write(person_json)



    except (Exception, Error) as err:
        print("?", err)




def ins_data():

    with open('postgres-records.json') as json_data:

        # use load() rather than loads() for JSON files
        record_list = json.load(json_data)

        for i in record_list:

            table_name = i
            sql_string = ''
            data_table = record_list[table_name]

            if type(data_table) == dict:
                fields = []
                data = ''

                for x, y in data_table.items():
                    fields.append(x)
                    data = data + "\'" + str(y) + "\',"

                data = data[:-1]
                table_name = i
                sql_string = 'INSERT INTO {} ({}) VALUES ({}); '.format(table_name, ','.join(fields), data)

                try:
                    # declare a new PostgreSQL connection object
                    conn = connect(database="campers4", user="postgres", password="postgres", host="127.0.0.1",
                                   port="5434")
                    # conn = connect(
                    #     port = 5434,
                    #     dbname = "campers4",
                    #     user = "postgres",
                    #     host = "127.0.0.1",
                    #     password = "postgres",
                    #     # attempt to connect for 3 seconds then raise exception
                    #     connect_timeout = 3)

                    cur = conn.cursor()
                    print("\ncreated cursor object:", cur)

                except (Exception, Error) as err:
                    print("\npsycopg2 connect error:", err)
                    conn = None
                    cur = None

                if cur != None:
                   try:
                       cur.execute(sql_string)
                       conn.commit()

                       print('\nfinished INSERT INTO execution')

                   except (Exception, Error) as error:
                        print("\nexecute_sql() error:", error)
                        conn.rollback()

                        # close the cursor and connection
                cur.close()
                conn.close()
            else:
                for r in data_table:
                    print(type(r))
                    fields = []
                    data = ''
                    for x, y in r.items():
                        fields.append(x)
                        data = data + "\'" + str(y) + "\',"

                    data = data[:-1]
                    table_name = i
                    sql_string = 'INSERT INTO {} ({}) VALUES ({}); '.format(table_name, ','.join(fields), data)

                    try:
                        # declare a new PostgreSQL connection object
                        conn = connect(database="campers4", user="postgres", password="postgres", host="127.0.0.1", port="5434")
                        # conn = connect(
                        #     port = 5434,
                        #     dbname="campers4",
                        #     user="postgres",
                        #     host="127.0.0.1",
                        #     password="postgres",
                        #     # attempt to connect for 3 seconds then raise exception
                        #     connect_timeout=3)

                        cur = conn.cursor()
                        print("\ncreated cursor object:", cur)

                    except (Exception, Error) as err:
                        print("\npsycopg2 connect error:", err)
                        conn = None
                        cur = None

                    if cur != None:

                        try:
                            cur.execute(sql_string)
                            conn.commit()

                            print('\nfinished INSERT INTO execution')

                        except (Exception, Error) as error:
                            print("\nexecute_sql() error:", error)
                            conn.rollback()

                            # close the cursor and connection
                    cur.close()
                    conn.close()


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    ins_data()


# See PyCharm help at https://www.jetbrains.com/help/pycharm/
