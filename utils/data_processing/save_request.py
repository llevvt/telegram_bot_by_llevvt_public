from config_data.pathes_data import history_path
import sqlite3
import os


def save_request(request_dict, user_id):
    if os.path.exists(history_path):
        with sqlite3.connect(r'{}'.format(history_path)) as database:
            cur = database.cursor()
            cur.execute("SELECT * FROM history WHERE userid='{}';".format(str(user_id)))
            results = cur.fetchall()
            if len(results) <= 9:
                add_new_object(request_dict, user_id)
            else:
                cur.execute("DELETE FROM history WHERE userid='{}'".format(user_id))
                database.commit()
                add_new_object(request_dict, user_id)
    else:
        add_new_object(request_dict, user_id)


def add_new_object(request_dict, user_id):
    new_tuple = (
        user_id, request_dict['url'], request_dict['name'], request_dict['city'],
        str(request_dict['rating']), str(request_dict['price'])
    )

    with sqlite3.connect(r'{}'.format(history_path)) as database:
        cur = database.cursor()
        cur.execute("""CREATE TABLE IF NOT EXISTS history( 
        userid INT,
        url TEXT,
        hotelname TEXT,
        city TEXT,
        rating TEXT,
        price TEXT);
        """)
        database.commit()
        cur.execute("INSERT INTO history VALUES(?,?,?,?,?,?);", new_tuple)
        database.commit()


