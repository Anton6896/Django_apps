"""
connect to psql server !
"""

import psycopg2
import random

r = random


def connect():  # populate event

    try:
        # connect to db
        con = psycopg2.connect(
            host="localhost",
            database="mmn_11",
            user="anton",
            password="6896180An!",    
            port=5432)

        cursor = con.cursor()
        # Print PostgreSQL Connection properties
        print ( con.get_dsn_parameters(),"\n")

        # Print PostgreSQL version
        cursor.execute("SELECT version();")
        record = cursor.fetchone()
        print("You are connected to - ", record,"\n")

    # # cursor
    # cur = con.cursor()

    # # Print PostgreSQL Connection properties
    # # print(con.get_dsn_parameters(), "\n")

    # # Print PostgreSQL version
    # cur.execute("SELECT version();")
    # record = cur.fetchone()
    # print("You are connected to - ", record, "\n")

    # # insert into event
    # # values ('fest_4', '3-5-19', '15:00');

    # cur.execute("select * from event ")
    # rows = cur.fetchall()  # tuples of data

    # for r in rows:
    #     # print(f"s#:{r[0]}  p#:{r[1]}  qun: {r[2]}")
    #     print(r)

    # #     insert to event :
    # fest = ['fest_1', 'fest_2', 'fest_3', 'fest_4', 'fest_5']

    # print('enter data ...')
    # for _ in range(10):
    #     data = f" insert into event " \
    #            f"values ('{random.choice(fest)}'," \
    #            f"'{random.randint(1, 11)}-{random.randint(1, 29)}-{random.randint(2019, 2020)}'," \
    #            f" '{random.randint(1, 23)}:{random.randint(1, 55)}')"

    #     cur.execute(data)

    # print('check data : ')

    # cur.execute("select * from event ")
    # rows = cur.fetchall()  # tuples of data

    # for r in rows:
    #     # print(f"s#:{r[0]}  p#:{r[1]}  qun: {r[2]}")
    #     print(r)

    # con.commit()
    # print('data crated')

    #         cursor = connection.cursor()
    #
    #     create_table_query = '''CREATE TABLE mobile
    #           (ID INT PRIMARY KEY     NOT NULL,
    #           MODEL           TEXT    NOT NULL,
    #           PRICE         REAL); '''
    #
    #     cursor.execute(create_table_query)
    #     connection.commit()
    #     print("Table created successfully in PostgreSQL ")

    except (Exception, psycopg2.Error) as error:
        print("Error while connecting to PostgreSQL", error)

    finally:
        # close db, cursor
        if (con):
            cur.close()
            con.close()


if __name__ == '__main__':
    connect()
    # fill_booked()
    pass
