import psycopg2
import logging


class Database:
    def __init__(self, data):
        self.data = data

    def check_connection(self):
        for db_name in self.data.keys():
            for rw, v in self.data[db_name].items():
                logging.info('Connecting to Database... (db_name={}, instance={}, host={}, port={})' .format(db_name, rw, v['host'], v['port']))

                try:
                    conn = psycopg2.connect(host=v['host'],
                                            dbname=db_name,
                                            user=self.data[db_name][rw]['username'],
                                            password=self.data[db_name][rw]['password'],
                                            port=v['port'])
                    cur = conn.cursor()
                    cur.execute('select 1')
                    rows = cur.fetchall()

                    if len(rows) > 0:
                        logging.info('Connection was successful. (db_name={}, instance={}, host={}, port={})' .format(db_name, rw, v['host'], v['port']))
                    else:
                        raise ConnectionError

                except Exception as e:
                    logging.error(e)
                    logging.error('Psycopg2 Connection failed. (db_name={}, instance={}, host={}, port={})' .format(db_name, rw, v['host'], v['port']))

